from datetime import datetime
from mapping import map_categories
def get_news_json(soup):

            title = soup.find('meta', property='og:title')
            url = soup.find('meta', property='og:url')
            category = soup.find('meta', property='article:section')
            newsSource = soup.find('meta', property='og:site_name')
            description = soup.find('meta', property='og:description')
            publishedDateTime = soup.find('meta', property='article:published_time')

            metadata = {}

            if url:
                metadata["url"] = url['content']
                #if url mapped then also create created date and time
                metadata["createdDateTime"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                metadata["url"] = None
                metadata["createdDateTime"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if title:
                metadata["title"] = title['content']
            else:
                metadata['title'] = None

            if category:
                metadata["category"] =map_categories(category['content'])
            else:
                metadata["category"] ="Others"

            if newsSource:
                metadata["newsSource"] = newsSource['content']
            else:
                metadata["newsSource"] = None

            if description:
                metadata["description"] = description['content']
            else:
                metadata["description"] = None

            if publishedDateTime:
                metadata["publishedDateTime"] = publishedDateTime['content']
            else:
                metadata["publishedDateTime"] = None

            return metadata