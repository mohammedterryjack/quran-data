BOOKS_IN_TANAKH = {
    "torah/genesis":"01","torah/exodus":"02","torah/leviticus":"03","torah/numbers":"04","torah/deuteronomy":"05",
    "prophets/joshua":"06","prophets/judges":"07","prophets/i%20samuel":"08a","prophets/ii%20samuel":"08b",
    "prophets/i%20kings":"09a","prophets/ii%20kings":"09b","prophets/isaiah":"10","prophets/jeremiah":"11",
    "prophets/ezekiel":"12","prophets/hosea":"13","prophets/joel":"14","prophets/amos":"15","prophets/obadiah":"16",
    "prophets/jonah":"17","prophets/micah":"18","prophets/nahum":"19","prophets/habakkuk":"20",
    "prophets/zephaniah":"21","prophets/haggai":"22","prophets/zechariah":"23","prophets/malachi":"24",
    "writings/i%20chronicles":"25a","writings/ii%20chronicles":"25b","writings/psalms":"26","writings/job":"27",
    "writings/proverbs":"28","writings/ruth":"29","writings/song%20of%20songs":"30","writings/ecclesiastes":"31",
    "writings/lamentations":"32","writings/esther":"33","writings/daniel":"34","writings/ezra":"35a","writings/nehemiah":"35b"
}

CHAPTERS_IN_TANAKH = {
    "torah/genesis":50,"torah/exodus":40,"torah/leviticus":27,"torah/numbers":36,"torah/deuteronomy":34,
    "prophets/joshua":24,"prophets/judges":21,"prophets/i%20samuel":31,"prophets/ii%20samuel":24,
    "prophets/i%20kings":22,"prophets/ii%20kings":25,"prophets/isaiah":66,"prophets/jeremiah":52,
    "prophets/ezekiel":48,"prophets/hosea":14,"prophets/joel":4,"prophets/amos":9,"prophets/obadiah":1,
    "prophets/jonah":4,"prophets/micah":7,"prophets/nahum":3,"prophets/habakkuk":3,
    "prophets/zephaniah":3,"prophets/haggai":2,"prophets/zechariah":14,"prophets/malachi":3,
    "writings/i%20chronicles":29,"writings/ii%20chronicles":36,"writings/psalms":150,"writings/job":42,
    "writings/proverbs":31,"writings/ruth":4,"writings/song%20of%20songs":8,"writings/ecclesiastes":12,
    "writings/lamentations":5,"writings/esther":10,"writings/daniel":12,"writings/ezra":10,"writings/nehemiah":13
}

class TanakhAudio:
    def __init__(self) -> None:
        self.URL = "http://www.mechon-mamre.org/mp3"
        self.AUDIO_FORMAT = "mp3"
        self.BOOKS = BOOKS_IN_TANAKH

    def url(self, cannon:str, book:str, chapter:int) -> str:
        """ get url of audio file for book """
        chapter_key = str(chapter)
        if len(chapter_key) == 3:
            a,b,c = chapter_key
            chapter_key = f"{chr(int(a+b)+87)}{c}"
        else:
            chapter_key = chapter_key.zfill(2)
        return f"{self.URL}/t{self.BOOKS.get(f'{cannon}/{book}')}{chapter_key}.{self.AUDIO_FORMAT}"

from requests import get

t = TanakhAudio()
for book_name in BOOKS_IN_TANAKH:
    cannon,book = book_name.split("/")
    max_chapter = CHAPTERS_IN_TANAKH[book_name]
    for chapter in range(1,max_chapter+1):
        path_to_save = f"bible_audio/mamre/{cannon}_{book}_{chapter}.mp3"
        URL_TO_DOWNLOAD = t.url(cannon,book,chapter)
        response = get(URL_TO_DOWNLOAD)
        with open(path_to_save,'wb') as f: 
            f.write(response.content)