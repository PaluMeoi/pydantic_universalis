from typing import Optional, Sequence

import pydantic
import requests
from pydantic import validate_call
from ratelimit import sleep_and_retry, limits

from .models.current import Current, MultiCurrent
from .models.history import History, MultiHistory

import logging

class Universalis:
    def __init__(self):
        self.base_url = "https://universalis.app"
        self.session = requests.session()

    @sleep_and_retry
    @limits(calls=25, period=1)
    def get(self, url, **kwargs) -> dict:
        """Wrapper around requests get adding rate limiting

        :param url: URL to request
        :return: Response Object
        """
        additional_args = {
            k: ",".join(v) if isinstance(v, Sequence) else v for k, v in kwargs.items()
        }
        response = self.session.get(url, params=additional_args)
        return response.json()

    def request_item(self, worldDcRegion: int | str, itemId: int, **kwargs) -> dict:
        url = self.base_url + f"/api/v2/{worldDcRegion}/{itemId}"
        response = self.get(url, **kwargs)
        return response.json()

    def item(
            self,
            worldDcRegion: int | str,
            itemId: int,
            listings: Optional[int] = None,
            entries: Optional[int] = None,
            noGst: Optional[bool] = None,
            hq: Optional[bool] = None,
            statsWithin: Optional[int] = None,
            entriesWithin: Optional[int] = None,
            fields: Optional[tuple[str]] = None,
    ) -> Current:
        url = self.base_url + f"/api/{worldDcRegion}/{itemId}"
        response = self.get(
            url,
            listings=listings,
            entries=entries,
            noGst=noGst,
            hq=hq,
            statsWithin=statsWithin,
            entriesWithin=entriesWithin,
            fields=fields,
        )
        return Current.model_validate(response)

    @validate_call
    def item_history(
            self,
            worldDcRegion: int | str,
            itemId: int,
            entriesToReturn: Optional[int] = None,
            statsWithin: Optional[int] = None,
            entriesWithin: Optional[int] = None,
    ) -> History:
        """
        Retrieves the history data for the requested item and world or data center.

        :param worldDcRegion: The world or data center to retrieve data for. This may be
            an ID or a name. Regions should be specified as Japan, Europe, North-America,
            Oceania, China, or 中国.
        :param itemId: The item ID of the item to retrieve data for.
        :param entriesToReturn: The number of entries to return per item. By default, this
            is set to 1800, but may be set to a maximum of 999999.
        :param statsWithin: The amount of time before now to calculate stats over,
            in milliseconds. By default, this is 7 days.
        :param entriesWithin: The amount of time before now to take entries within, in
            seconds. Negative values will be ignored.
        :return: A History object representing the returned data
        """
        url = self.base_url + f"/api/v2/history/{worldDcRegion}/{itemId}"
        response = self.get(
            url,
            entriesToReturn=entriesToReturn,
            statsWithin=statsWithin,
            entriesWithin=entriesWithin,
        )

        return History.model_validate(response)

    def items(
            self,
            worldDcRegion: int | str,
            itemIds: Sequence[int],
            listings: Optional[int] = None,
            entries: Optional[int] = None,
            noGst: Optional[bool] = None,
            hq: Optional[bool] = None,
            statsWithin: Optional[int] = None,
            entriesWithin: Optional[int] = None,
            fields: Optional[list[str]] = None,
    ) -> MultiCurrent:
        itemIds = list(set(itemIds))
        if len(itemIds) <= 100:
            _itemIds = ",".join([str(_itemID) for _itemID in itemIds])
            url = self.base_url + f"/api/v2/{worldDcRegion}/{_itemIds}"
            response = self.get(
                url,
                listings=listings,
                entries=entries,
                noGst=noGst,
                hq=hq,
                statsWithin=statsWithin,
                entriesWithin=entriesWithin,
                fields=fields,
            )
            if len(itemIds) > 1:
                return MultiCurrent.model_validate(response)
            else:
                # Changing the request into a "fake" MultiCurrent if only one item is requested
                logging.debug(f"Creating a fake MultiCurrent for item ID {itemIds[0]}")
                return self.make_multi("current", response)
        else:
            return self.many_items(
                worldDcRegion,
                itemIds,
                listings=listings,
                entries=entries,
                noGst=noGst,
                hq=hq,
                statsWithin=statsWithin,
                entriesWithin=entriesWithin,
                fields=fields,
            )

    @staticmethod
    def make_multi(model: str, response: dict):
        if model == "history":
            single = History.model_validate(response)
            _model = MultiHistory
        else:
            single = Current.model_validate(response)
            _model = MultiCurrent

        return _model.model_validate(
            {
                "itemIDs":         [single.itemID],
                "items":           {single.itemID: single},
                "worldID":         single.worldID,
                "dcName":          single.dcName,
                "regionName":      single.regionName,
                "unresolvedItems": [],
                "worldName":       single.worldName,
            }
        )

    def many_items(
            self,
            worldDcRegion: int | str,
            itemIds: Sequence[int],
            listings: Optional[int] = None,
            entries: Optional[int] = None,
            noGst: Optional[bool] = None,
            hq: Optional[bool] = None,
            statsWithin: Optional[int] = None,
            entriesWithin: Optional[int] = None,
            fields: Optional[list[str]] = None,
    ) -> MultiCurrent:
        """
        A helper function for handling requests longer than 100 itemIDs
        """
        itemIds = [itemIds[i: i + 100] for i in range(0, len(itemIds), 100)]
        request_itemIds = itemIds.pop()
        response = self.items(
            worldDcRegion,
            request_itemIds,
            listings=listings,
            entries=entries,
            noGst=noGst,
            hq=hq,
            statsWithin=statsWithin,
            entriesWithin=entriesWithin,
            fields=fields,
        )
        results = MultiCurrent.model_validate(response)
        for request_itemIds in itemIds:
            new_items = self.items(
                worldDcRegion,
                request_itemIds,
                listings=listings,
                entries=entries,
                noGst=noGst,
                hq=hq,
                statsWithin=statsWithin,
                entriesWithin=entriesWithin,
                fields=fields,
            )
            results.itemIDs.extend(new_items.itemIDs)
            results.items.update(new_items.items)
            results.unresolvedItems.extend(new_items.unresolvedItems)
        return results

    def request_items_history(
            self, worldDcRegion: int | str, itemIds: Sequence[int], **kwargs
    ) -> dict:
        itemIds = ",".join([str(_itemID) for _itemID in itemIds])
        url = self.base_url + f"/api/v2/history/{worldDcRegion}/{itemIds}"
        response = self.get(url, **kwargs)
        return response.json()

    @validate_call
    def items_history(
            self,
            worldDcRegion: int | str,
            itemIds: Sequence[int],
            entriesToReturn: Optional[int] = None,
            statsWithin: Optional[int] = None,
            entriesWithin: Optional[int] = None,
    ) -> MultiHistory:
        if len(itemIds) <= 100:
            _itemIds = ",".join([str(_itemID) for _itemID in itemIds])
            url = self.base_url + f"/api/v2/history/{worldDcRegion}/{_itemIds}"
            response = self.get(url, entriesToReturn=entriesToReturn, statsWithin=statsWithin,
                                entriesWithin=entriesWithin)
            if len(itemIds) > 1:
                return MultiHistory.model_validate(response)
            else:
                return self.make_multi("history", response)
        else:
            return self.many_items_history(
                worldDcRegion, itemIds, entriesToReturn, statsWithin, entriesWithin
            )

    def many_items_history(
            self,
            worldDcRegion: int | str,
            itemIds: Sequence[int],
            entriesToReturn: Optional[int] = None,
            statsWithin: Optional[int] = None,
            entriesWithin: Optional[int] = None,
    ):
        itemIds = [itemIds[i: i + 100] for i in range(0, len(itemIds), 100)]
        all_history = [
            self.items_history(
                worldDcRegion, request_ids, entriesToReturn, statsWithin, entriesWithin
            )
            for request_ids in itemIds
        ]
        result = all_history.pop()
        for history in all_history:
            result.itemIDs.extend(history.itemIDs)
            result.unresolvedItems.extend(history.unresolvedItems)
            result.items.update(history.items)
        return result


if __name__ == "__main__":
    uni = Universalis()

    itemIDs = [39687, 39692, 39697, 39702, 39635]

    data = uni.items(
        "Excalibur", [2],
    )
    print(data)
