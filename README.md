# Detection Method for Distributed Web-Crawlers: a Long-tail Threshold Model

This paper proposes an advanced countermeasure against distributed web-crawlers. We investigated other methods for crawler detection and analyzed how distributed crawlers can bypass these methods. Our method can detect distributed crawlers by focusing on the property that web traffic follows the power distribution. When we sort web pages by the number of requests, most of requests are concentrated on the most frequently requested web pages. In addition, there will be some web pages that normal users do not generally request. But crawlers will request for these web pages because their algorithms are intended to request iteratively by parsing web pages to collect every item the crawlers encounter. Therefore, we can assume that if some IP addresses are frequently used to request the web pages that are located in the long-tail area of a power distribution graph, those IP addresses can be classified as crawler nodes. The experimental results with NASA web traffic data showed that our method was effective in identifying distributed crawlers with 0.0275% false positives when a conventional frequency-based detection method shows 2.882% false positives with an equal access threshold.


### Security and Communication Networks
- Volume 2018, Article ID 9065424, 7 pages
- https://doi.org/10.1155/2018/9065424
