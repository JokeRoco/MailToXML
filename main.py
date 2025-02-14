import jinja2 as jj
from datetime import datetime
import LandNameInfo


class OfferRequest:
    def __init__(self, offer_string: str):
        lines = offer_string.split("\n")
        del lines[len(lines)-1]
        # Parsen der Metadaten
        meta = lines[1].split("\t")

        self.date = meta[0]
        self.salutation = meta[1]
        self.firstname = meta[2]
        self.lastname = meta[3]
        self.company = meta[4]
        self.sw_customer_id = meta[5]
        self.email = meta[6]
        self.street = meta[7]
        self.city = meta[8]
        self.city_code = meta[9]
        self.country = LandNameInfo.GetLandNameInfo(meta[10]).get_Kuerzel()
        self.order_id = "A_"+str(int((datetime.strptime(self.date, '%d.%m.%Y %H:%M:%S')-datetime(1970,1,1)).total_seconds()))  #Erstellung einer Order-ID anhand des Zeitstempels

        # Parsen der Artikel
        self.articles = []
        for line in lines[2:]:
            self.articles.append(
                {
                    "amount": line.split(" x ")[0],
                    "no": line.split(" (")[-1].split(") ")[0],
                    "price": line.split(" - ")[-1].split(" EUR")[0]
                }
            )

    def get_xml(self):
        env = jj.Environment()
        template = env.from_string(
            """
                <basket>
                    <shop>main</shop>
                    <cpOrderId/>
                    <comment/>
                    <deliveryType>0</deliveryType>
                    <language>DE</language>
                    <deliveryoption>1</deliveryoption>
                    <orderID>{{ req.order_id }}</orderID>
                    <save>1</save>
                    <paymentId>0</paymentId>
                    <positions>
                        {% for article in req.articles %}
                        <position>
                            <price>{{ article["price"] }}</price>
                            <customerarticlenumber/>
                            <ordernumber>{{ article["no"] }}</ordernumber>
                            <amount>{{ article["amount"] }}</amount>
                        </position>
                        {% endfor %}
                    </positions>
                    <customer>
                        <shopwareId>{{ req.sw_customer_id }}</shopwareId>
                        <group>B</group>
                        <personal>
                            <type/>
                            <salutation>{{ req.salutation }}</salutation>
                            <firstname>{{ req.firstname }}</firstname>
                            <lastname>{{ req.lastname }}</lastname>
                            <email>{{ req.email }}</email>
                            <number>{{ req.sw_customer_id }}</number>
                        </personal>
                        <billing>
                            <salutation>{{ req.salutation }}</salutation>
                            <firstname>{{ req.firstname }}</firstname>
                            <lastname>{{ req.lastname }}</lastname>
                            <company>{{ req.company }}</company>
                            <department/>
                            <vatId/>
                            <street>{{ req.street }}</street>
                            <zipcode>{{ req.city_code }}</zipcode>
                            <city>{{ req.city }}</city>
                            <country>{{ req.country }}</country>
                        </billing>
                        <shipping>
                            <salutation>{{ req.salutation }}</salutation>
                            <firstname>{{ req.firstname }}</firstname>
                            <lastname>{{ req.lastname }}</lastname>
                            <company>{{ req.company }}</company>
                            <department/>
                            <vatId/>
                            <street>{{ req.street }}</street>
                            <zipcode>{{ req.city_code }}</zipcode>
                            <city>{{ req.city }}</city>
                            <country>{{ req.country }}</country>
                        </shipping>
                    </customer>
                </basket>
            """
        )
        return template.render(req=self)

'''
test = EmailXFromFolderF.GetEmailX_FromFolderF(1, "R.Coburger@joke.de\Posteingang\Aufgaben")
d=str(test.order_info).replace('\r', '')
req=OfferRequest(d)

f = open(req.order_id+".xml","wb")                 #öffnen/erstellen einer xml-Datei
f.write(bytes(req.get_xml(), 'utf-8'))      #xml-Datei mit Inhalt füllen
f.close()*/'''

