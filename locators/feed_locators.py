class FeedLocators:
    TOTAL_ORDERS_COUNT = "//p[contains(@class, 'OrderFeed_number')][1]"
    TODAY_ORDERS_COUNT = "//p[contains(@class, 'OrderFeed_number')][2]"
    ORDER_IN_PROGRESS = "//ul[contains(@class, 'OrderFeed_orderListReady')]//li[contains(text(), '{}')]"
    ORDER_CARD = "//div[contains(@class, 'OrderHistory_link')][1]"