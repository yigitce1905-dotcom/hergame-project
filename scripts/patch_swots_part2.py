# patch_swots_part2.py  — Players 53-99 (second half of missing SWOTs)
# Run from project root: python scripts/patch_swots_part2.py
import json

TS = "2026-05-28T09:00:00.000000+00:00"
MODEL = "claude-sonnet-4-5"

def sw(s, w, o, t):
    return {"strengths": s, "weaknesses": w, "opportunities": o, "threats": t,
            "generated_at": TS, "model": MODEL}

SWOTS = {
"Azzurra Gallo": sw(
    ["Juventus gibi Serie A Femminile'nin en rekabetçi kulübünde bulunması, stoper pozisyonunda üst düzey taktiksel eğitim ve disipline maruz kaldığını kanıtlar.",
     "69/100 FM26 notu, İtalyan savunma ekolünün önem verdiği kapama verimliliği ve pozisyon disiplini açısından umut vadeden bir profil ortaya koymaktadır.",
     "Juventus altyapısının sağladığı bireysel gelişim programları ve elit antrenör kadrosu, potansiyelini somutlaştırma sürecini desteklemektedir."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut kondisyon ve form düzeyinin belirsiz kalmasına yol açmaktadır.",
     "Juventus'taki yüksek rekabet, oyuncunun ilk 11'e girebilmesini uzun vadede zorlaştırmakta ve gelişim ivmesini yavaşlatmaktadır.",
     "İstatistiklerin tümüyle sıfırda olması, geriden oyun kurma kalitesi ve hücum katkısını değerlendirmeyi olanaksız kılıyor."],
    ["Juventus formasıyla Serie A'da alacağı ilk maç süresi, kariyerini hızla ivmelendirmek için paha biçilmez bir platform oluşturabilir.",
     "Juventus'un küresel marka değeri, oyuncunun scout ağlarına kısa sürede dahil olmasını ve transfer piyasasında değer kazanmasını sağlar.",
     "İtalya Milli Takımı altyapıları için ideal bir aday profili çizmekte, ulusal kariyer kapısını kolayca zorlayabilir."],
    ["Juventus'ta uzun süre yedek kalmak, 69'luk potansiyelin körelmesine ve piyasa değerinin gerilemesine neden olabilir.",
     "Daha az rekabetçi bir ortama kiralık gitme fırsatı kaçırılırsa, gelişim için kritik yıllar boşa geçebilir.",
     "Serie A'nın fiziksel sertliğine hazırlık olmaksızın aniden forma çıkılması, kritik hatalar ve özgüven kaybı riskini barındırır."]
),

"Solveig Slemmem": sw(
    ["Sağ ve sol bek ile kanat bek (D/WB RL) pozisyonlarındaki çift yönlü esneklik, Lyn'ın savunma hattında hem sağ hem sol koridorda operasyonel çözüm sunmaktadır.",
     "69/100 FM26 notu, Norveç ekolünün getirdiği güçlü savunma otomatizmi ve hücum-savunma geçiş hızıyla desteklenen makul bir profil ortaya koyuyor.",
     "Lyn'ın Norveç ligindeki köklü yapısı, taktiksel disiplin ve rekabet odaklı gelişim ortamı açısından değerli bir platform sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hem sağ hem sol koridorda oynatılabilmesi, belirli bir uzmanlık alanının oluşmamasına ve transfer profilinin net olmamasına yol açabilir.",
     "Gol ve asist istatistiklerinin sıfırda olması, kanat bek profilinde beklenen hücuma katkı etkinliğinin test edilmediğini göstermektedir."],
    ["İkili bek esnekliği, savunma derinliği arayan kulüpler için maliyet etkin bir transfer çözümü sunmaktadır.",
     "Norveç Milli Takımı'nın kanat bek rotasyonuna dahil olma şansı, uluslararası kariyer kapısını açabilir.",
     "Lyn'dan kiralık bir transfer, düzenli maç süresi kazanarak değerini somutlaştırma fırsatı doğurabilir."],
    ["Çift koridordaki esneklik, üst liglerde spesifik bek pozisyonu arayan kulüpler tarafından göz ardı edilmesine neden olabilir.",
     "Norveç liginin sınırlı uluslararası görünürlüğü, scout ilgisinin gecikmesine zemin hazırlayabilir.",
     "Uzun maçsız dönem, kanat beklerde kritik olan hız patlayıcılığı ve çapraz top kalitesi üzerinde olumsuz etki yaratabilir."]
),

"Nikayla Small": sw(
    ["Sağ/merkez orta saha ve ofansif orta saha (M RC, AM C) kombinasyonundaki çift boyutlu yetkinlik, AFC Toronto'nun orta sahasına hem savunma filtresi hem yaratıcı pasör kimliği katıyor.",
     "Kanada futbolunun NWSL merkezli gelişim altyapısı, oyuncuya rekabetçi bir ortamda taktiksel ve fiziksel olgunlaşma imkânı sağlamaktadır.",
     "69/100 FM26 puanı, orta sahada top kazanma ile oyun açma dengesini koruyan üst sıralarda değerlendirilen bir kariyer profili ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form düzeyi ve takım sistemine entegrasyon konusundaki belirsizliği artırmaktadır.",
     "İstatistiklerinin tamamının sıfırda olması, pas isabeti, top kazanma oranı ve hücum katkısını nesnel olarak analiz etmeyi olanaksız kılıyor.",
     "Fiziksel verilerinin bilinmemesi, özellikle orta saha mücadelelerinde güç ve dayanıklılık konusunda değerlendirme yapmayı güçleştiriyor."],
    ["NWSL'in artan küresel görünürlüğü, Kanada merkezli bu profil için Avrupa kulüplerinin scouting ilgisini çekme fırsatı sunmaktadır.",
     "Kanada Milli Takımı'nın orta sahada genç nesil arayışı, ulusal kariyer yolunu kolaylaştırabilir.",
     "Hem kontrol hem yaratıcılık sunabilen profili, farklı taktik sistemler kullanan kulüpler için uyarlanabilir bir transfer hedefi oluşturuyor."],
    ["NWSL'in Avrupa büyük liglerinden taktiksel ve fiziksel olarak ayrışması, üst liga transferinde uyum güçlüklerine zemin hazırlayabilir.",
     "Uzun maçsız dönem, orta saha oyuncularında kritik olan oyun ritmi ve otomatik tepki hızını köreltme riski taşımaktadır.",
     "Kanada'nın Avrupa piyasasındaki scout temsil gücünün sınırlı olması, transfer fırsatlarının zamanında değerlendirilmesini zorlaştırabilir."]
),

"Natalia Oleszkiewicz": sw(
    ["Trabzonspor formasıyla Türk Kadın Futbol Süper Ligi'nde resmi maç oynama deneyimi, uluslararası adaptasyon kapasitesini ve mesleki olgunluğunu kanıtlamaktadır.",
     "Polonyalı santrafor olarak FM26'da 69/100 scout notu almış olması, gol bölgesinde ciddi bir baskı unsuru oluşturma ve pozisyon bulma kapasitesine işaret eder.",
     "170 cm boy ve sağ ayak tercihi ile klasik santrafor profilini destekleyen fiziksel altyapıya sahip olup bitiricilik açısından istikrarlı bir tehdit oluşturuyor."],
    ["Bu sezonda yalnızca 2 resmi maçta süre alması, aktif maç ritmi ve kondisyon açısından ciddi bir eksiklik yaratmaktadır.",
     "Trabzonspor formasıyla henüz gol veya asist üretememiş olması, bitiricilik ve üçüncü bölge etkinliği konusunda soru işareti doğurmaktadır.",
     "Türk liginin Avrupa büyük ligleriyle olan rekabet farkı, üst seviyeli savunmaların sertliğine uyum konusunda belirsizlik taşımaktadır."],
    ["Türk ligindeki yabancı uyruklu oyuncu kotasının sağladığı avantaj, Avrupa'dan geçiş köprüsü görevi görebilecek diğer liglere transfer kapısını aralayabilir.",
     "Polonya Milli Takımı kadrosunda düzenli yer bulduğu takdirde, uluslararası maçlar aracılığıyla kariyer görünürlüğünü artırabilir.",
     "Trabzonspor'dan yapılacak olası bir transfer, daha fazla süre alarak FM26'daki 69'luk potansiyelini sahaya yansıtma fırsatı sunabilir."],
    ["Türk liginin Avrupa'daki görece düşük temsil gücü, yabancı kulüplerin ilgisini çekmek için ek kanıt ve daha fazla saha saati gerektirmektedir.",
     "Az maç süresiyle yüksek beklenti arasındaki uçurum, oyuncu üzerinde gereksiz baskı oluşturabilir ve özgüven kaybına zemin hazırlayabilir.",
     "Sözleşme ve pasaport koşulları, Türk liginden Avrupa'nın rekabetçi piyasalarına geçişi zaman zaman karmaşık hale getirebilir."]
),

"Laurel Ansbrow": sw(
    ["Merkez defans (D C) pozisyonunda Boston Legacy'nin NWSL ortamında forma mücadelesi vermesi, Kuzey Amerika'nın fiziksel ve taktiksel zorluklarıyla yüzleşme kapasitesini kanıtlar.",
     "68/100 FM26 notu, Amerikan futbol ekolünün getirdiği atakçı fizik ve sert savunma anlayışıyla birleşen güçlü bir bek profili çizmektedir.",
     "NWSL'in artan küresel görünürlüğü, Boston merkezli bu oyuncunun Avrupa scout ekranlarına çıkması için değerli bir platform sunuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon düzeyi konusundaki değerlendirmeyi güçleştirmektedir.",
     "Gol ve asist istatistiklerinin sıfırda olması, stoper pozisyonunda beklenen geriden oyun kurma kalitesini analiz etmeyi zorlaştırmaktadır.",
     "Fiziksel verilerinin bilinmemesi, özellikle hava topu mücadelelerinde dominant ya da dezavantajlı konumu belirsiz bırakmaktadır."],
    ["NWSL'de alacağı düzenli maç süresi, Avrupa kulüplerinin dikkatini çekecek analitik verilerin birikmesini sağlayacaktır.",
     "ABD pasaportunun WSL gibi liglere geçişte herhangi bir vize engeli oluşturmaması, transfer sürecini basitleştirmektedir.",
     "NWSL'in yükselen medya değeri ve yayın ortaklıkları, oyuncunun kariyer profilini küresel ölçekte güçlendirme fırsatı sunuyor."],
    ["NWSL'den Avrupa büyük liglerine geçişte taktiksel ve fiziksel tempo farkı, adaptasyon döneminde beklenmedik güçlükler yaratabilir.",
     "Uzun maçsız dönem, stoper pozisyonunda kritik olan savunma koordinasyonu ve hata düzeltme otomatizminde gerilemeye yol açabilir.",
     "Amerikalı stoper profilinin Avrupa'da yeterince bilinmemesi, transfer ilgisinin gecikmesine zemin hazırlayabilir."]
),

"Ilayda Açıkgöz": sw(
    ["Merkez ve ofansif orta saha (M/AM C) pozisyonundaki ikili yetkinlik, Eintracht Frankfurt'un orta sahasına hem top kesme hem yaratıcı pas sağlayan değerli bir profil katıyor.",
     "Alman–Türk ikili kimliği, her iki ülkenin milli takım altyapıları için değerli bir aday konumuna getirmekte ve kariyer seçeneklerini genişletmektedir.",
     "68/100 FM26 notu ve Bundesliga Frankfurt altyapısı, teknik gelişim için üst düzey bir ortamın sağlandığını kanıtlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, aktif form ve maç kondisyonu konusundaki değerlendirmeyi olanaksız kılmaktadır.",
     "İstatistiklerinin tamamının sıfırda olması, oyun kurma kalitesi ve son bölge üretkenliği hakkında nesnel analiz yapmayı güçleştiriyor.",
     "Frankfurt'taki yoğun orta saha rekabeti, forma almasını uzun vadede zorlaştırabilir ve gelişim ivmesini sekteye uğratabilir."],
    ["Bundesliga platformu ve Frankfurt'un uluslararası kulüp turnuvalarındaki varlığı, Avrupa genelinde görünürlük sağlıyor.",
     "Türk Milli Takımı'nın orta saha arayışında güçlü bir aday profili çizmekte, uluslararası kariyer kapısını zorlayabilir.",
     "Frankfurt'tan kiralık bir transfer veya aktif oynayabileceği bir kulübe geçiş, 68'lik potansiyelini sahaya yansıtma fırsatı sunabilir."],
    ["Bundesliga'nın fiziksel ve taktiksel yoğunluğuna uyum sağlamak, özellikle maçsız uzun dönem sonrasında ciddi adaptasyon güçlükleri yaratabilir.",
     "Frankfurt orta sahasındaki uzun süreli yedeklik, oyuncunun kendini ispat etme sürecini geciktirerek piyasa değerini olumsuz etkileyebilir.",
     "İkili milli takım seçeneğinin yarattığı belirsizlik, kariyerin erken döneminde odak kaybına ve motivasyon düşüklüğüne zemin hazırlayabilir."]
),

"Ronja Arnesen": sw(
    ["Sağ kanat bek, sağ/merkez orta saha ve sağ/sol/merkez hücum sahası (WB R, M RC, AM RLC) genelindeki geniş çok yönlülük, sağ koridorda ve orta sahada kapsamlı taktiksel seçenekler sunuyor.",
     "Vålerenga'da Norveç liginin rekabetçi ortamında bu esnekliği geliştirmesi, yüksek uyum kapasitesi ve futbol zekasına sahip olduğunu kanıtlamaktadır.",
     "68/100 FM26 puanı, sahada beş farklı pozisyondaki bu yetkinliğin derinlemesine bir teknik altyapıyla desteklendiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form düzeyi ve mevcut hazırlık konusundaki değerlendirmeyi güçleştirmektedir.",
     "Geniş pozisyon yelpazesi, belirli bir rol için spesifik marka değeri oluşturulmasını engelleyerek transfer sürecini karmaşıklaştırabilir.",
     "Hücum istatistiklerinin sıfırda olması, özellikle ofansif rollerde beklenen son bölge üretkenliğinin test edilmediğini göstermektedir."],
    ["Çift koridor ve orta sahayı kapsayan esneklik, farklı taktik sistemler kullanan Avrupa kulüpleri için cazip bir transfer profili oluşturuyor.",
     "Norveç Milli Takımı'nda joker oyuncu rolünü üstlenerek uluslararası kariyer yolunu açabilir.",
     "Vålerenga'da düzenli süre yakaladığında, birden fazla pozisyondaki etkinliğiyle scout ilgisini hızla çekebilir."],
    ["Pozisyon bolluğu, üst ligde net bir rol arayan teknik direktörler tarafından göz ardı edilmesine neden olabilir.",
     "Uzun maçsız dönem, bu kadar geniş pozisyon repertuvarını sürdüren oyuncuda kas ve koordinasyon düzeyinde belirgin gerilemeye yol açabilir.",
     "Norveç liginin Batı Avrupa ile kıyaslandığında sınırlı uluslararası temsil gücü, scout faaliyetlerinin gecikmesine zemin hazırlayabilir."]
),

"Nelly Da Cruz Rodrigues": sw(
    ["Sağ bek ve sağ kanat bek (D RC, WB R) pozisyonlarındaki ikili yetkinlik, FC Nantes'ın sağ koridorunda hem savunma güvenliği hem hücum derinliği sunuyor.",
     "Portekiz–Fransa çift kültürel arka planı, D1 Féminine standartlarına hızlıca uyum sağlama kapasitesini ve çok yönlü taktiksel farkındalığı desteklemektedir.",
     "67/100 FM26 notu, sağ koridor ağırlıklı modern bek profilinde üst sıralarda değerlendirilen, gelişime açık bir kariyer eğrisine işaret ediyor."],
    ["Bu sezon resmi maçta süre alamamış olması, kondisyon ve maç ritmi açısından değerlendirme yapmayı güçleştirmektedir.",
     "Hücum istatistiklerinin sıfırda olması, sağ kanat bek profilinde beklenen son bölge çapraz topları ve asist katkısını sorgulatmaktadır.",
     "Fiziksel verilerin belirsizliği, özellikle hız ve çapraz top kalitesi konusundaki gerçek kapasiteyi analiz etmeyi güçleştiriyor."],
    ["D1 Féminine'nin küresel scout trafiği ve yayın ağları, oyuncunun erken kariyer döneminde Avrupa piyasalarına dahil olmasını kolaylaştırır.",
     "Portekiz Milli Takımı için seçilebilirlik, Avrupa platformlarında görünürlük kazanarak kariyer değerini artırma fırsatı sunmaktadır.",
     "Sağ koridor çok yönlülüğü, pozisyon derinliği arayan orta bütçeli Avrupa kulüpleri için uygun maliyetli bir transfer seçeneği oluşturur."],
    ["D1 Féminine'nin yoğun sağ bek rekabeti, form almanın önünde kalıcı bir engel oluşturabilir.",
     "Uzun maçsız dönem, kanat beklerde kritik olan patlayıcı koşu ve çapraz top kapasitesinin körelmesine yol açabilir.",
     "Portekiz'in Fransa piyasasındaki sınırlı scout temsili, transfer fırsatlarının zamanında değerlendirilmesini geciktirebilir."]
),

"Katja Skupień": sw(
    ["Kanat bek, orta ve ofansif orta saha (WB/M/AM RL) genelinde çift koridorda esneklik, Sassuolo'nun kanat oyununa geniş taktiksel seçenekler kazandırmaktadır.",
     "Polonya'dan Serie A Femminile'ye geçiş, önemli bir taktiksel adaptasyon kapasitesi ve disiplin sergilediğini kanıtlar.",
     "67/100 FM26 notu, hem savunma hem hücumda aktif yer alan dinamik kanat profilinde değer taşıdığını ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, kondisyon ve form konusundaki değerlendirmeyi olanaksız kılmaktadır.",
     "İstatistiklerin tümünün sıfırda olması, kanat pozisyonlarında beklenen üretkenliği analiz etmeyi güçleştirmektedir.",
     "Fiziksel verilerin bilinmemesi, hız ve dayanıklılık konusundaki gerçek kapasiteyi belirsiz bırakmaktadır."],
    ["Sassuolo'nun İtalyan ligindeki konumu ve Avrupa kupası katılımları, scout görünürlüğü için stratejik fırsatlar yaratmaktadır.",
     "Polonya Milli Takımı'nın kanat ihtiyacı, oyuncuya uluslararası kariyer basamağını tırmanma şansı sunmaktadır.",
     "Çift koridordaki esneklik, transfer piyasasında birden fazla pozisyon için talep görmesini sağlar."],
    ["Serie A'nın yoğun kanat oyuncu rekabeti, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir.",
     "Uzun maçsız dönem, kanat oyuncularında hayati önem taşıyan patlayıcı koşu kapasitesini olumsuz etkileyebilir.",
     "İtalya'nın yabancı uyruklu oyunculara yönelik kota kısıtlamaları, mevcut sözleşme planlamasını zorlaştırabilir."]
),

"Bente Fischer": sw(
    ["Sol ve merkez bek (D LC) pozisyonlarındaki esneklik, Carl Zeiss Jena'nın savunma hattında sol aksın her iki rolünü karşılama kapasitesi sunuyor.",
     "Alman futbol ekolünden gelmesi, taktiksel disiplin ve pressing verimliliği konularında güçlü bir temel sağlamaktadır.",
     "67/100 FM26 notu, 2. Bundesliga standardında sol–merkez bek kombinasyonunda makul bir kariyer potansiyeline sahip olduğunu gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücum istatistiklerinin sıfırda olması, geriden oyun kurma kalitesi ve duran top katkısını analiz etmeyi zorlaştırıyor.",
     "Fiziksel verilerin belirsizliği, hava topu ve fiziksel güç gerektiren mücadelelerdeki etkinliği hakkında belirsizlik yaratmaktadır."],
    ["2. Bundesliga'nın Almanya scout ağıyla yakın ilişkisi, oyuncunun Bundesliga ekranlarına çıkmasını erken dönemde kolaylaştırabilir.",
     "Almanya Milli Takımı altyapısı için güçlü bir sol bek adayı olan oyuncu, ulusal kariyer yolunu zorlayabilir.",
     "Sol–merkez bek esnekliği, farklı savunma sistemleri kullanan kulüpler için cazip bir maliyet–fayda profili oluşturuyor."],
    ["2. Bundesliga'dan Bundesliga'ya geçiş farkı, ilk dönemde performans düşüklüğüne zemin hazırlayabilir.",
     "Jena'nın savunma rekabeti, forma alma sürecini uzatarak gelişim ivmesini sekteye uğratabilir.",
     "Maçsız uzun dönem, sol bekte kritik olan hız ve pozisyon alma otomatizmini köreltme riski taşımaktadır."]
),

"Bruna Ramos": sw(
    ["Sağ bek ve sağ kanat bek (D/WB R) pozisyonlarındaki ikili yetkinlik, Torreense'nin sağ koridorunda savunma ve hücum dengesi kuran bir profil sunuyor.",
     "Portekiz kadın futbolunun Avrupa'daki artan görünürlüğü ve Sporting/Benfica gibi büyük kulüplerin etkisiyle gelişen lig altyapısı, oyuncunun taktiksel gelişimine katkı sağlamaktadır.",
     "67/100 FM26 notu, Portekiz liginin rekabetçi ortamında sağ koridor dominansı açısından değer taşıdığını ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form düzeyi ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Portekiz birinci liginin Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, üst liga transferinde adaptasyon sorunlarına yol açabilir.",
     "İstatistiklerin tümünün sıfırda olması, sağ kanat bek profilinde beklenen hücuma katkı etkinliğini değerlendirmeyi olanaksız kılıyor."],
    ["Portekiz Milli Takımı'nın sağ bek rotasyonuna dahil olarak uluslararası görünürlük kazanabilir.",
     "D1 Féminine veya İspanya Primera Iberdrola gibi üst liglere geçiş fırsatı bulunması halinde, taktiksel olgunluk kazanma kapısı açılır.",
     "Torreense'nin Portekiz ligindeki konumu, oyuncunun daha büyük bütçeli yerli kulüplerin ilgisini çekmesini kolaylaştırabilir."],
    ["Portekiz liginin sınırlı uluslararası medya görünürlüğü, yabancı kulüplerin ilgisinin gecikmesine zemin hazırlayabilir.",
     "Uzun maçsız dönem, kanat beklerde kritik olan çapraz top ve patlayıcı koşu kapasitesinde form kaybına neden olabilir.",
     "Torreense'nin görece düşük profili, oyuncunun kariyer hedeflerini gerçekleştirmesi için ek tanıtım ve görünürlük gerektiriyor."]
),

"Julia Jędrzejewska": sw(
    ["Sağ bek, kanat bek ve orta saha (D/WB/M R) pozisyonlarındaki geniş yelpaze, Śląsk Wrocław'ın sağ koridorunda savunmadan hücuma kadar her rolü kapsayan çok boyutlu bir profil sunuyor.",
     "Polonyalı bir oyuncu olarak yerel futbol ekolünün getirdiği güçlü mücadele azmi ve fiziksel dayanıklılık, rekabetçi ortama uyum kapasitesini desteklemektedir.",
     "67/100 FM26 notu, sağ koridordaki bu üçlü rol yetkinliğinde değer taşıdığını ve gelişime açık bir kariyer eğrisi çizdiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki belirsizliği artırmaktadır.",
     "Üç farklı pozisyondaki esneklik, belirli bir uzmanlık alanının oluşmamasına ve net bir transfer profili çizilememesine neden olabilir.",
     "İstatistiklerin sıfırda olması, hücum katkısı ve savunma etkinliğini değerlendirmeyi olanaksız kılmaktadır."],
    ["Polonya Milli Takımı için çok yönlü sağ koridor alternatifi olarak değerlendirilebilir ve uluslararası kariyer kapısını zorlayabilir.",
     "Sağ koridordaki üçlü rol esnekliği, farklı sistemler kullanan Avrupa kulüpleri için pratik bir transfer çözümü oluşturuyor.",
     "Śląsk Wrocław'dan Polonya'nın daha büyük kulüplerine ya da yurt dışına yapılacak transfer, kariyer ivmesini hızlandırabilir."],
    ["Polonya liginin Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, üst liga transferinde beklenmedik adaptasyon güçlükleri yaratabilir.",
     "Pozisyon belirsizliği, üst ligde spesifik rol arayan teknik direktörler tarafından göz ardı edilmesine neden olabilir.",
     "Uzun maçsız dönem, sağ koridorda kritik olan hız ve patlayıcı geçiş kapasitesini olumsuz etkileyebilir."]
),

"Meret Günster": sw(
    ["Defansif ve merkez orta saha (DM, M C) pozisyonlarındaki yetkinlik, 1. FC Nürnberg'in orta sahası için hem savunma filtresi hem top dağıtıcısı kimliğini sunmaktadır.",
     "Almanya futbol ekolünden gelen oyuncu, pressing verimliliği ve taktiksel disiplin konusunda güçlü bir temel oluşturmuştur.",
     "67/100 FM26 notu, 2. Bundesliga standardında orta saha kontrolcüsü rolünde kariyer değeri taşıdığını gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut form ve rekabete uyum konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücum istatistiklerinin sıfırda olması, DM–M profilinin yanı sıra oyun açma ve skor üretimine katkı konusundaki etkinliği belirsizleştiriyor.",
     "Fiziksel verilerinin bilinmemesi, orta saha mücadelelerindeki güç ve dayanıklılık açısından net analiz yapmayı engelliyor."],
    ["2. Bundesliga'nın Almanya scout ağı, Bundesliga geçişi için erken fırsat sağlamaktadır.",
     "Nürnberg'de düzenli maç süresi yakalanması, 67'lik potansiyeli somutlaştırmak için doğru bir zemin oluşturacaktır.",
     "Almanya Milli Takımı altyapısı için genç DM alternatifi olarak değerlendirilebilir."],
    ["2. Bundesliga'nın tempolu rekabeti, maçsız dönem sonrasında aniden adaptasyonu zorlaştırabilir.",
     "Nürnberg'deki yoğun orta saha rekabeti, forma şansını kısıtlayarak gelişim ivmesini yavaşlatabilir.",
     "Almanya'nın derin orta saha stoku, üst ligde öne çıkmayı istatistiksel kanıt olmaksızın güçleştiriyor."]
),

"Kristin Krammer": sw(
    ["1. FC Nürnberg'de Alman futbolunun teknik kaleci eğitim ekolüne maruz kalmak, refleks kapasitesi ve ceza sahası yönetimi açısından güçlü bir altyapı sağlamaktadır.",
     "67/100 FM26 notu, Avusturyalı bu kaleciyi Bundesliga standardının altındaki liglerde bile rekabetçi bir profil olarak değerlendirmektedir.",
     "Avusturya–Almanya çift kültürel arka planı, her iki ülkenin milli takım altyapıları için değerli bir aday konumuna getiriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, zamanlama ve refleks açısından maç ritmi kaybı yaratmaktadır.",
     "Nürnberg'deki kaleci rekabetinin yüksekliği, forma almasını uzun vadede zorlaştırabilir.",
     "Fiziksel verilerin bilinmemesi, özellikle uzun çıkışlar ve hava topu hakimiyeti konusundaki etkinliği belirsizleştiriyor."],
    ["Avusturya Milli Takımı'nın kaleci rotasyonuna dahil olmak, uluslararası kariyer kapısını aralayabilir.",
     "Nürnberg'den kiralık bir transfer, düzenli maç süresi kazanarak 67'lik potansiyelini somutlaştırma fırsatı sunabilir.",
     "Alman kaleci ekolündeki gelişim, daha büyük liglerin ilgisini erken dönemde çekebilir."],
    ["Bundesliga'nın derin kaleci kadrosu, forma alma sürecini ciddi ölçüde zorlaştırmaktadır.",
     "Uzun maçsız dönem, kaleciler için kritik olan refleks keskinliği ve anlık tepki hızını olumsuz etkiler.",
     "Maçsız sürecin yarattığı özgüven eksikliği, ilk forma şansında kritik hatalar yapma riskini artırabilir."]
),

"Hannah Mesch": sw(
    ["Sol orta ve sol/sağ ofansif orta saha (M L, AM RL) kombinasyonundaki yetkinlik, Carl Zeiss Jena'nın sol aksında yaratıcı ve dinamik bir kanat tehdidi oluşturuyor.",
     "Alman futbol altyapısından gelmesi, disiplinli pressing anlayışı ve top taşıma kapasitesi açısından güçlü bir temel sağlamaktadır.",
     "67/100 FM26 notu, 2. Bundesliga ortamında sol kanat yaratıcılığı ve oyun açma becerisiyle değer taşıdığını gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücum istatistiklerinin sıfırda olması, son bölge üretkenliği ve asist kalitesini analiz etmeyi olanaksız kılıyor.",
     "Fiziksel verilerinin bilinmemesi, sol kanatta bir-bir mücadele ve hız konusundaki etkinliği belirsizleştiriyor."],
    ["2. Bundesliga platformu, Bundesliga kulüplerinin scout ağlarına erken dönemde dahil olmayı kolaylaştırıyor.",
     "Almanya Milli Takımı altyapısı için sol kanat alternatifi olarak değerlendirilebilir.",
     "Sol–sağ kanat esnekliği, farklı taktik sistemlerde oynayan kulüpler için cazip bir transfer profili oluşturuyor."],
    ["Almanya'nın derin kanat oyuncu stoku, üst ligde öne çıkmayı istatistiksel kanıt olmaksızın güçleştiriyor.",
     "Uzun maçsız dönem, kanat oyuncularında kritik olan patlayıcı koşu kapasitesini olumsuz etkiler.",
     "Jena'nın görece düşük medya profili, scout ilgisinin gecikmesine zemin hazırlayabilir."]
),

"Magnaba Folquet": sw(
    ["Hem merkez hem de ofansif orta saha (M/AM C) pozisyonlarındaki ikili yetkinlik, Havre FC'nin orta sahasında hem kontrol hem yaratıcılık sağlayan profil sunuyor.",
     "D1 Féminine'nin rekabetçi ortamında forma mücadelesi vermesi, Fransız kadın futbolunun üst düzey taktiksel standartlarında gelişme fırsatı yakaladığını gösteriyor.",
     "67/100 FM26 notu, Fransız futbol ekolünün getirdiği teknik incelik ve oyun okumayla desteklenen bir orta saha kimliği ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Gol ve asist istatistiklerinin sıfırda olması, son bölge üretkenliğini ve pas kalitesini nesnel olarak analiz etmeyi zorlaştırıyor.",
     "Fiziksel verilerin bilinmemesi, orta saha mücadelelerindeki güç ve dayanıklılık konusunda belirsizlik yaratmaktadır."],
    ["D1 Féminine platformu, Avrupa kulüplerinin scout faaliyetleri için ideal bir vitrin sunuyor.",
     "Fransa Milli Takımı altyapısı için orta saha alternatifi olarak değerlendirilebilir.",
     "Merkez–ofansif ikili profili, farklı oyun anlayışları için uyarlanabilir bir transfer hedefi oluşturuyor."],
    ["D1 Féminine'nin rekabetçi orta saha yoğunluğu, forma alma sürecini uzatabilir.",
     "Uzun maçsız dönem, orta saha oyuncularında kritik olan ritim ve top duyarlılığını olumsuz etkiler.",
     "Fransız ligindeki güçlü Fransız orta saha profili kalabalığı, yabancı uyruklu ya da az bilinen oyuncu için öne çıkmayı zorlaştırıyor."]
),

"Carla Tays": sw(
    ["Merkez defans (D C) pozisyonunda Palmeiras gibi Güney Amerika'nın en prestijli kulüplerinden birinde forma giymesi, fiziksel rekabet ortamına uyum kapasitesini kanıtlar.",
     "66/100 FM26 notu ve Brezilya futbol ekolünün getirdiği güçlü topçuluk temeli, stoper pozisyonunda teknik değer taşıdığını gösteriyor.",
     "Palmeiras'ın Brezilya'daki marka değeri ve uluslararası kupa deneyimi, oyuncuya küresel scout ağlarına erken girme fırsatı sunuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, kondisyon ve form konusundaki değerlendirmeyi güçleştirmektedir.",
     "Brezilya'nın Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, üst liga transferinde adaptasyon sorunlarına zemin hazırlayabilir.",
     "İstatistiklerin sıfırda olması, geriden oyun kurma kalitesi ve savunma etkinliğini analiz etmeyi güçleştiriyor."],
    ["Palmeiras'ın Libertadores Kupası gibi uluslararası platformlardaki varlığı, oyuncunun daha geniş bir scout ağına dahil olmasını sağlıyor.",
     "Brezilya Milli Takımı'nın genç savunma kadrosu için potansiyel bir aday olan oyuncu, ulusal kariyer yolunu açabilir.",
     "NWSL ya da Avrupa'nın orta bütçeli kulüplerine yapılacak transfer, kariyer ivmesini ciddi ölçüde artırabilir."],
    ["Güney Amerika'nın Avrupa scout ağlarına sınırlı erişimi, transfer fırsatlarının gecikmesine neden olabilir.",
     "Uzun maçsız dönem, stoper pozisyonunda kritik olan savunma koordinasyonunu ve otomatizmi olumsuz etkiler.",
     "Brezilya'nın stoper rekabetinin yoğunluğu, oyuncunun görünürlük kazanmasını ve öne çıkmasını zorlaştırabilir."]
),

"Natalia Radkiewicz": sw(
    ["Pogoń Szczecin'de Polonya birinci liginin kaleci pozisyonunda görev alması, ulusal standartlarda rekabetçi bir kalecilik pratiği kazandırmaktadır.",
     "66/100 FM26 notu, Polonya kaleci ekolünden gelen refleks kapasitesi ve ceza sahası yönetimi açısından değer taşıdığını gösteriyor.",
     "Polonya'nın Avrupa kulüpleriyle artan etkileşimi, oyuncuya daha geniş scout ağlarına dahil olma fırsatı sunmaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, maç ritmi ve kondisyon konusundaki değerlendirmeyi olanaksız kılıyor.",
     "Polonya liginin Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, üst liga transferinde adaptasyon sorunu yaratabilir.",
     "İstatistiklerin sıfırda olması, kaleci performansını nesnel olarak değerlendirmeyi güçleştiriyor."],
    ["Polonya Milli Takımı'nın kaleci rotasyonuna dahil olarak uluslararası kariyer kapısını zorlayabilir.",
     "Pogoń Szczecin'den yapılacak bir kiralama, düzenli maç süresi kazanarak 66'lık potansiyelini somutlaştırma fırsatı sunabilir.",
     "Polonya'nın Avrupa'daki artan futbol görünürlüğü, scout ilgisinin yakın gelecekte artmasına zemin hazırlıyor."],
    ["Polonya liginin sınırlı uluslararası medya görünürlüğü, yabancı kulüplerin ilgisini çekmek için ek çaba gerektiriyor.",
     "Uzun maçsız dönem, kaleciler için hayati önem taşıyan refleks keskinliğini ve anlık tepki hızını olumsuz etkiler.",
     "Pogoń Szczecin'deki kaleci rekabeti, uzun vadede forma alma şansını kısıtlayabilir."]
),

"Paula Flach": sw(
    ["Sol bek (D L) pozisyonunda SGS Essen'in Bundesliga standardındaki savunma kurgusunda görev alması, taktiksel disiplin ve sol aksın kontrolü açısından güçlü bir altyapı sağlıyor.",
     "65/100 FM26 notu, Alman savunma ekolünün getirdiği disiplin ve ikili mücadele kapasitesiyle makul bir kariyer değeri taşıdığını gösteriyor.",
     "SGS Essen'in Bundesliga'daki deneyimli teknik kadrosu, bireysel gelişim için değerli bir mentörlük ortamı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücum istatistiklerinin sıfırda olması, sol bek profilinde beklenen kanat katkısı ve asist üretimini sorgulatmaktadır.",
     "Fiziksel verilerinin bilinmemesi, sol koridorda bir-bir mücadele ve hız konusundaki etkinliği belirsizleştiriyor."],
    ["Bundesliga platformunun Alman scout ağıyla güçlü bağlantısı, daha büyük kulüplerin radarına girmeyi kolaylaştırır.",
     "Almanya Milli Takımı altyapısı için sol bek alternatifi olarak değerlendirilebilir.",
     "SGS Essen'den düzenli maç süresi yakalandığında, 65'lik potansiyeli sahaya yansıtma fırsatı ortaya çıkacaktır."],
    ["Bundesliga'nın derin sol bek stoku, öne çıkmayı istatistiksel kanıt olmaksızın güçleştiriyor.",
     "Uzun maçsız dönem, sol bekte kritik olan hız ve pozisyon alma otomatizmini olumsuz etkiler.",
     "Essen'deki yoğun savunma rekabeti, forma alma sürecini uzatarak kariyer planlarını sekteye uğratabilir."]
),

"Clara Wibaut": sw(
    ["Reims gibi D1 Féminine'nin köklü kulüplerinden birinde bulunması, Fransız kaleci ekolünün teknik eğitimine ve rekabetçi ortama maruz kaldığını gösteriyor.",
     "65/100 FM26 notu, Fransız kaleciler için önem taşıyan ayakla oyun kurma ve baskı altında pas dağıtma becerileri açısından değer taşıdığını ortaya koyuyor.",
     "D1 Féminine standardında şekillenmiş teknik kalecilik altyapısı, farklı liglere transferde uyum kolaylığı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, maç ritmi ve reaksiyon kapasitesi konusundaki değerlendirmeyi güçleştiriyor.",
     "Reims'deki kaleci rekabetinin yoğunluğu, forma almasını uzun vadede zorlaştırabilir.",
     "Fiziksel verilerin bilinmemesi, uzun çıkışlar ve hava topu hakimiyeti konusunda belirsizlik yaratmaktadır."],
    ["D1 Féminine'nin aktif scout trafiği, oyuncunun Avrupa piyasasına erken dahil olmasını sağlar.",
     "Fransa Milli Takımı altyapısı için kaleci alternatifi olarak değerlendirilebilir.",
     "Reims'den kiralık bir transfer, düzenli maç süresi kazanarak 65'lik potansiyelini somutlaştırma fırsatı sunabilir."],
    ["D1 Féminine'nin rekabetçi kaleci kadrosu, forma alma sürecini uzatabilir.",
     "Uzun maçsız dönem, kaleciler için kritik olan refleks ve zamanlama konusunda gerileme riski taşır.",
     "Reims'den uzak kalma süreci, Fransa'daki diğer kaleci adayları karşısında konumunu zayıflatabilir."]
),

"Diána Németh": sw(
    ["Sol bek ve sol kanat bek (D/WB L) pozisyonlarındaki esneklik, RB Leipzig'in sol koridorunda hem savunma hem hücum katkısı sunan değerli bir profil oluşturuyor.",
     "65/100 FM26 notu ve Macar futbol ekolünden Bundesliga'ya uzanan kariyer yolculuğu, adaptasyon kapasitesi ve mesleki kararlılık açısından güçlü bir profil çiziyor.",
     "Leipzig'in genç oyuncuları geliştirmeye yönelik sistematik altyapısı, 65'lik potansiyeli somutlaştırma sürecini desteklemektedir."],
    ["Bu sezon resmi maçta süre alamamış olması, kondisyon ve form konusundaki değerlendirmeyi güçleştirmektedir.",
     "Macaristan'ın Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, Bundesliga rekabetine uyumda güçlükler yaratabilir.",
     "İstatistiklerin sıfırda olması, sol bek profilinde beklenen hücum katkısını değerlendirmeyi olanaksız kılıyor."],
    ["Leipzig'in Bundesliga'daki güçlü marka değeri ve scout ağı, oyuncunun Avrupa çapında tanınmasını hızlandırabilir.",
     "Macaristan Milli Takımı'nın sol bek rotasyonuna dahil olarak uluslararası kariyer kapısını zorlayabilir.",
     "Leipzig altyapısındaki bireysel gelişim programları, 65'lik potansiyeli gerçeğe dönüştürme sürecini destekler."],
    ["Bundesliga'nın fiziksel tempo ve rekabetine uyum sağlamakta zorlanmak, uzun vadeli kadro planlamasının dışına düşme riskini barındırır.",
     "Leipzig sol koridorundaki mevcut rekabet, forma alma şansını kısıtlayabilir.",
     "Macaristan'ın Avrupa piyasasındaki sınırlı scout temsili, transfer fırsatlarının gecikmesine zemin hazırlayabilir."]
),

"Adriana Achcińska": sw(
    ["Defansif ve merkez orta saha (DM, M C) pozisyonlarındaki yetkinlik, 1. FC Köln'ün orta sahasında top kazanma ve oyun inşası açısından çift boyutlu katkı sunuyor.",
     "65/100 FM26 notu ve Polonyalı bir oyuncu olarak Almanya'da forma mücadelesi vermesi, uluslararası adaptasyon kapasitesini kanıtlamaktadır.",
     "Köln'ün Bundesliga standardındaki taktiksel altyapısı, orta saha disiplini ve pressing verimliliği açısından güçlü bir eğitim ortamı sağlıyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "İstatistiklerin tümünün sıfırda olması, pas kalitesi ve top kazanma oranını nesnel olarak analiz etmeyi olanaksız kılıyor.",
     "Fiziksel verilerinin bilinmemesi, özellikle orta saha fiziksel mücadelelerindeki dayanıklılık konusunda belirsizlik yaratıyor."],
    ["Bundesliga platformu ve Köln'ün uluslararası kulüp kimliği, Avrupa genelinde görünürlük fırsatı sunuyor.",
     "Polonya Milli Takımı'nın orta saha rotasyonuna dahil olarak uluslararası kariyer kapısını zorlayabilir.",
     "Köln'den kiralık bir transfer, düzenli maç süresi kazanarak 65'lik potansiyelini somutlaştırma imkânı sunabilir."],
    ["Bundesliga'nın yoğun orta saha rekabeti, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir.",
     "Uzun maçsız dönem, orta saha oyuncularında kritik olan ritim ve otomatik tepki hızını köreltebilir.",
     "Almanya'nın derin orta saha stoku, üst ligde öne çıkmayı istatistiksel kanıt olmaksızın güçleştiriyor."]
),

"Rebekka Salfelder": sw(
    ["Sol kanat bek ve sol orta saha (WB/M L) pozisyonlarındaki esneklik, bonservis gerektirmeksizin anında katkı sunan maliyet etkin bir sol koridor çözümü oluşturuyor.",
     "Almanya futbol ekolünden gelen serbest oyuncu, Bundesliga standartlarında sol koridorun hem savunma hem hücum gerekliliklerini karşılama kapasitesine sahip.",
     "65/100 FM26 notu, serbest oyuncu olmasına karşın teknik kapasitesinin üst sıralarda değerlendirildiğini, yatırım değeri açısından güçlü bir profil oluşturduğunu gösteriyor."],
    ["Serbest oyuncu statüsü, herhangi bir takım sistemine entegre olmamış olmasından kaynaklanan kondisyon eksikliği ve ritim kaybı riskini beraberinde getirir.",
     "Bu sezon resmi maçta süre alamamış olması, aktif formunu ve sahaya hazırlık düzeyini değerlendirmeyi güçleştiriyor.",
     "Fiziksel verilerinin bilinmemesi, sol koridorda hız, güç ve hava topu etkinliği konusunda belirsizlik yaratmaktadır."],
    ["Bonservis bedelsiz transfer edilebilmesi, bütçe kısıtlaması olan kulüpler için anlık bir sol koridor çözümü sunuyor.",
     "Sol kanat bek–orta saha kombinasyonu, farklı taktik sistemlerde kısa sürede çoklu pozisyonda katkı yapma kapasitesi sunuyor.",
     "Alman futbol ekolünden gelen bu profil, Bundesliga veya 2. Bundesliga kulüpleri için test edilmeye değer uygun maliyetli bir transfer seçeneği oluşturuyor."],
    ["Uzun süre takım sisteminden uzak kalmak, sözleşme müzakerelerinde beklentilerin düşük tutulmasına yol açabilir.",
     "Serbest oyuncu durumu, bazen piyasa değerinin düşüklüğüyle özdeşleştirilmesine neden olabilir.",
     "Rekabetçi bir transferde şartları belirleyecek baskı gücünün olmaması, ideal olmayan bir kulüp ya da sisteme dahil olma riskini barındırır."]
),

"Nina Varga": sw(
    ["Merkez defans (D C) pozisyonunda Medimurje'nin Hırvatistan ligi ortamında forma giymesi, ulusal düzeyde rekabetçi savunma deneyimi kazandırmaktadır.",
     "64/100 FM26 notu, Hırvatistan futbol ekolünün getirdiği güçlü mücadele azmi ve bireysel kapama becerisiyle makul bir kariyer değeri taşıdığını gösteriyor.",
     "Hırvatistan'ın Avrupa futbolundaki artan görünürlüğü ve genç yeteneklere yönelik artan ilgi, oyuncunun keşfedilme şansını artırmaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hırvatistan liginin Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, üst liga transferinde adaptasyon güçlükleri yaratabilir.",
     "İstatistiklerin sıfırda olması, savunma etkinliği ve geriden oyun kurma kalitesini analiz etmeyi güçleştiriyor."],
    ["Hırvatistan Milli Takımı'nın savunma kadrosu için potansiyel bir aday olarak değerlendirilebilir.",
     "Medimurje'den daha rekabetçi bir Hırvat kulübüne ya da yurt dışına transfer, kariyer ivmesini artırabilir.",
     "Hırvatistan'ın Avrupa futbol ekonomisindeki büyüyen rolü, oyuncunun erken dönemde keşfedilme şansını destekliyor."],
    ["Hırvatistan liginin sınırlı uluslararası medya görünürlüğü, scout ilgisinin gecikmesine zemin hazırlayabilir.",
     "Uzun maçsız dönem, stoper pozisyonunda kritik olan savunma koordinasyonunu ve otomatizmi olumsuz etkiler.",
     "Medimurje'nin görece düşük profili, kariyer hedeflerini gerçekleştirmek için ek tanıtım ve görünürlük gerektiriyor."]
),

"Ana Sušak": sw(
    ["Sağ bek, kanat bek ve orta saha (D/WB/M R) pozisyonlarındaki üçlü yetkinlik, Agram'ın sağ koridorunda savunmadan hücuma kadar her rolü kapsayan dinamik bir profil sunuyor.",
     "64/100 FM26 notu, Hırvatistan futbol ekolünden gelen güçlü bireysel mücadele ve adaptasyon kapasitesiyle makul bir kariyer değeri taşıdığını gösteriyor.",
     "Hırvatistan'ın Avrupa futbolundaki artan görünürlüğü, genç yeteneklerin keşfedilme sürecini hızlandırmaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Üç farklı pozisyondaki esneklik, belirli bir uzmanlık alanının oluşmamasına yol açabilir.",
     "İstatistiklerin sıfırda olması, sağ koridorda beklenen hücum katkısını değerlendirmeyi olanaksız kılıyor."],
    ["Hırvatistan Milli Takımı için sağ koridor alternatifi olarak değerlendirilebilir.",
     "Daha rekabetçi bir Hırvat kulübüne ya da yurt dışına transfer, kariyer ivmesini artırabilir.",
     "Sağ koridordaki üçlü rol esnekliği, farklı sistemler kullanan kulüpler için cazip bir transfer profili oluşturuyor."],
    ["Hırvatistan liginin sınırlı uluslararası görünürlüğü, scout ilgisinin gecikmesine zemin hazırlayabilir.",
     "Pozisyon belirsizliği, üst ligde spesifik rol arayan teknik direktörler tarafından göz ardı edilmesine neden olabilir.",
     "Agram'ın görece düşük profili, oyuncunun kariyer hedeflerini gerçekleştirmesi için ek tanıtım gerektiriyor."]
),

"Julie Swierot": sw(
    ["Defansif ve merkez orta saha (DM, M C) pozisyonlarındaki yetkinlik, OLL'nin orta sahasında hem savunma kontrolü hem oyun inşası sağlayan değerli bir profil sunuyor.",
     "Fransa futbol ekolünden gelmesi, taktiksel disiplin ve pressing verimliliği konularında güçlü bir temel sağlamaktadır.",
     "64/100 FM26 notu, Fransız orta saha profillerinde top kazanma ve oyun kurma dengesi açısından makul kariyer değeri taşıdığını gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "OLL'nin D1 Féminine'deki görece düşük profili, scout ilgisinin gecikmesine zemin hazırlıyor.",
     "İstatistiklerin sıfırda olması, pas kalitesi ve oyun kurma etkinliğini analiz etmeyi güçleştiriyor."],
    ["Fransa'nın gelişen kadın futbol ekosistemi, D2 Féminine'den D1'e çıkış yolu için uygun zemini destekliyor.",
     "D1'de düzenli maç süresi yakalandığında, Fransız Milli Takımı altyapıları için orta saha alternatifi olarak değerlendirilebilir.",
     "DM–M ikili profili, farklı taktik sistemler için uyarlanabilir bir transfer hedefi oluşturuyor."],
    ["Fransa'nın derin orta saha oyuncu stoku, öne çıkmayı istatistiksel kanıt olmaksızın güçleştiriyor.",
     "Uzun maçsız dönem, orta saha oyuncularında kritik olan ritim ve tepki hızını olumsuz etkiler.",
     "OLL'nin görece düşük profili, kariyer hedeflerini gerçekleştirmek için ek görünürlük gerektiriyor."]
),

"Nina Kajzba": sw(
    ["Klasik santrafor (ST C) pozisyonunda Parma Calcio'nun Serie A Femminile ortamında forma mücadelesi veren oyuncu, İtalyan liginin zorlu rekabetine maruz kaldığını gösteriyor.",
     "Slovenya'nın gelişen futbol kültürü ve 64/100 FM26 notu, gol bölgesinde ciddi bir tehdit unsuru oluşturma kapasitesine sahip olduğuna işaret ediyor.",
     "Serie A Femminile'nin yüksek taktiksel standartları, oyuncunun savunmaların sertliğine karşı dayanıklılık geliştirmesine yardımcı olmaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, gol üretimi ve maç kondisyonu konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücum istatistiklerinin sıfırda olması, birincil rolü olan bitiricilik ve gol üretimi konusunda soru işaretleri doğuruyor.",
     "Fiziksel verilerin bilinmemesi, özellikle hava topu ve güç mücadelelerindeki etkinliği belirsizleştiriyor."],
    ["Serie A Femminile'nin uluslararası scout ilgisi, oyuncunun Avrupa piyasasına erken dahil olmasını kolaylaştırır.",
     "Slovenya Milli Takımı'nın santrafor ihtiyacı, ulusal kariyer kapısını zorlama fırsatı sunuyor.",
     "Parma'dan alacağı düzenli maç süresi, 64'lük potansiyelini somutlaştırma imkânı sağlayabilir."],
    ["Serie A'nın zorlu savunma anlayışı, santrafor pozisyonunda maçsız dönem sonrasında aniden forma çıkılmasını güçleştirebilir.",
     "Parma'nın yoğun hücum rekabeti, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir.",
     "İtalya'nın yerli oyunculara öncelik verme eğilimi, yabancı uyruklu bir santrafor için ek mücadele gerektiriyor."]
),

"Reese Tappan": sw(
    ["Merkez defans (D C) pozisyonunda Spokane'nin NWSL bağlantılı yapısında forma mücadelesi veren oyuncu, Kuzey Amerika'nın fiziksel ve taktiksel ortamına uyum kapasitesini gösteriyor.",
     "64/100 FM26 notu, ABD futbol ekolünün getirdiği atletizm ve güçlü bireysel kapama becerisiyle makul bir kariyer değeri taşıdığını ortaya koyuyor.",
     "NWSL'in artan küresel görünürlüğü ve gelişen altyapısı, oyuncunun erken kariyer döneminde keşfedilme şansını artırıyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Spokane'nin görece düşük medya profili, scout ilgisinin gecikmesine zemin hazırlıyor.",
     "İstatistiklerin sıfırda olması, savunma etkinliği ve geriden oyun açma kalitesini analiz etmeyi güçleştiriyor."],
    ["NWSL gelişim ligleri, oyuncunun daha büyük Kuzey Amerika kulüplerinin radarına girmesini kolaylaştırıyor.",
     "ABD Milli Takımı altyapıları için potansiyel bir stoper adayı olan oyuncu, ulusal kariyer yolunu zorlayabilir.",
     "NWSL'de alacağı düzenli maç süresi, 64'lük potansiyelini somutlaştırarak kariyer değerini artırabilir."],
    ["NWSL'in Avrupa büyük liglerinden taktiksel ve fiziksel olarak ayrışması, üst liga transferinde adaptasyon güçlükleri yaratabilir.",
     "Uzun maçsız dönem, stoper pozisyonunda kritik olan savunma koordinasyonunu olumsuz etkiler.",
     "Spokane'nin düşük profili, oyuncunun kariyer hedeflerini gerçekleştirmesi için ek görünürlük gerektiriyor."]
),

"Julia Mickenhagen": sw(
    ["Sol bek ve sol kanat bek (D/WB L) pozisyonlarındaki esneklik, Bayer 04 Leverkusen'ın sol koridorunda hem savunma güvenliği hem hücum derinliği sağlıyor.",
     "Bundesliga standartlarındaki Leverkusen altyapısında yetişmesi, yüksek taktiksel disiplin ve rekabet ortamına uyum kapasitesini kanıtlar.",
     "64/100 FM26 notu, sol koridor profilinde Bundesliga ortamında değer taşıdığını ve gelişime açık bir kariyer eğrisi çizdiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Bundesliga'nın yoğun sol bek rekabeti, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir.",
     "İstatistiklerin sıfırda olması, sol koridorda beklenen hücum katkısını değerlendirmeyi olanaksız kılıyor."],
    ["Leverkusen'ın Bundesliga ve Avrupa kupalarındaki güçlü varlığı, scout görünürlüğü için değerli bir platform sunuyor.",
     "Almanya Milli Takımı altyapısı için sol bek alternatifi olarak değerlendirilebilir.",
     "Leverkusen'den kiralık bir transfer, düzenli maç süresi kazanarak potansiyelini somutlaştırma fırsatı sunabilir."],
    ["Leverkusen'ın derin sol kanat kadrosu, forma alma sürecini ciddi ölçüde zorlaştırmaktadır.",
     "Uzun maçsız dönem, sol bekte kritik olan hız ve pozisyon alma otomatizmini olumsuz etkiler.",
     "Almanya'nın derin sol bek stoku, üst ligde öne çıkmayı istatistiksel kanıt olmaksızın güçleştiriyor."]
),

"Rose Kadzere": sw(
    ["Sağ açık hücumcu ve santrafor (AM R, ST C) pozisyonlarındaki ikili yetkinlik, Montpellier'nin hücumunda hem kanat hem merkez tehdidi oluşturma kapasitesi sunuyor.",
     "Malawi kökenli bir oyuncu olarak D1 Féminine'de forma mücadelesi vermesi, Afrika'dan Avrupa'ya başarılı bir adaptasyon hikâyesini temsil ediyor.",
     "63/100 FM26 notu, dribbling kapasitesi ve hız ağırlıklı hücum profilinde kariyer değeri taşıdığını gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Gol ve asist istatistiklerinin sıfırda olması, hücum pozisyonlarında beklenen üretkenliği analiz etmeyi olanaksız kılıyor.",
     "Fiziksel verilerin bilinmemesi, özellikle hız ve savunmaların sertliğine karşı dayanıklılık konusunda belirsizlik yaratıyor."],
    ["Malawi Milli Takımı'nın Afrika Kupası platformu, uluslararası görünürlük kazanarak kariyer profilini güçlendirme fırsatı sunuyor.",
     "Fransa ligindeki başarılı uyumu, başka Avrupa liglerinin de ilgisini çekebilir.",
     "Sağ kanat ve santrafor kombinasyonu, farklı hücum sistemleri kullanan kulüpler için cazip bir transfer hedefi oluşturuyor."],
    ["D1 Féminine'nin rekabetçi hücum yapısı, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir.",
     "Uzun maçsız dönem, hız ağırlıklı hücum profilinde form ve patlayıcılık kaybına neden olabilir.",
     "Malawi'nin Avrupa scout ağlarına sınırlı erişimi, transfer fırsatlarının gecikmesine zemin hazırlayabilir."]
),

"Barbara Živković": sw(
    ["Defansif, merkez/sağ orta saha ve sağ ofansif orta saha (DM, M RC, AM R) genelindeki geniş yelpaze, Hajduk'un orta sahasında çok boyutlu taktiksel seçenekler sunuyor.",
     "63/100 FM26 notu ve Hırvatistan'ın rekabetçi futbol liginde forma mücadelesi vermesi, orta sahada çok yönlü bir profil sergilediğini ortaya koyuyor.",
     "Hırvatistan'ın Avrupa futbolundaki artan görünürlüğü ve genç yeteneklere yönelik artan ilgi, oyuncunun keşfedilme şansını destekliyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Geniş pozisyon yelpazesi, belirli bir uzmanlık alanının oluşmamasına yol açabilir.",
     "İstatistiklerin sıfırda olması, orta sahada beklenen katkıyı değerlendirmeyi olanaksız kılıyor."],
    ["Hırvatistan Milli Takımı için çok yönlü orta saha alternatifi olarak değerlendirilebilir.",
     "Hajduk Split'in Hırvatistan ligindeki prestijli konumu, scout görünürlüğü için değerli bir platform sunuyor.",
     "Farklı orta saha pozisyonlarındaki esneklik, farklı sistemler kullanan Avrupa kulüpleri için cazip bir transfer profili oluşturuyor."],
    ["Hırvatistan liginin sınırlı uluslararası görünürlüğü, scout ilgisinin gecikmesine zemin hazırlayabilir.",
     "Pozisyon belirsizliği, üst ligde spesifik rol arayan teknik direktörler tarafından göz ardı edilmesine neden olabilir.",
     "Uzun maçsız dönem, orta saha oyuncularında kritik olan ritim ve tepki hızını olumsuz etkiler."]
),

"Manuela Sciabica": sw(
    ["Defansif, merkez/sağ/sol orta saha ve sağ/sol ofansif orta saha (DM, M RLC, AM RL) genelindeki istisnai çok yönlülük, Juventus'un orta sahasına geniş taktiksel seçenekler kazandırıyor.",
     "Juventus altyapısında yetişmesi, Serie A Femminile'nin en yüksek taktiksel standartlarında gelişim fırsatı sunmaktadır.",
     "63/100 FM26 notu, bu geniş pozisyon yelpazesininin derinlemesine bir teknik altyapıyla desteklendiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Juventus'taki yoğun orta saha rekabeti, forma alma sürecini uzun vadede zorlaştırabilir.",
     "Geniş pozisyon yelpazesi, belirli bir uzmanlık alanının oluşmamasına yol açabilir."],
    ["Juventus'un küresel marka değeri, oyuncunun scout ağlarına hızla dahil olmasını sağlar.",
     "İtalya Milli Takımı altyapısı için çok yönlü orta saha alternatifi olarak değerlendirilebilir.",
     "Juventus'tan kiralık bir transfer, düzenli maç süresi kazanarak potansiyelini somutlaştırma fırsatı sunabilir."],
    ["Juventus'ta uzun süre yedek kalmak, 63'lük potansiyelin körelmesine ve piyasa değerinin gerilemesine neden olabilir.",
     "Serie A'nın yoğun orta saha rekabeti, forma alma sürecini uzatarak gelişim ivmesini sekteye uğratabilir.",
     "Pozisyon belirsizliği, teknik direktörlerin belirli bir taktik sistemde oyuncuyu konumlandırmasını güçleştirebilir."]
),

"Fanney Birkisdóttir": sw(
    ["BK Häcken gibi İsveç Damallsvenskan'ın en rekabetçi kulüplerinden birinde bulunması, yüksek düzeyli kalecilik rekabetine ve taktiksel eğitime maruz kaldığını gösteriyor.",
     "63/100 FM26 notu, İzlanda kaleci ekolünden gelen refleks kapasitesi ve ceza sahası yönetimi açısından makul kariyer değeri taşıdığını ortaya koyuyor.",
     "İzlanda'nın İskandinav kadın futbolundaki güçlü temsilciliği, oyuncuya uluslararası kariyer kapısını zorlama fırsatı sunuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, maç ritmi ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "BK Häcken'deki kaleci rekabetinin yoğunluğu, forma almasını uzun vadede zorlaştırabilir.",
     "Fiziksel verilerin bilinmemesi, özellikle uzun çıkışlar ve hava topu hakimiyeti konusunda belirsizlik yaratıyor."],
    ["İzlanda Milli Takımı'nın kaleci rotasyonuna dahil olarak uluslararası kariyer kapısını zorlayabilir.",
     "BK Häcken'den kiralık bir transfer, düzenli maç süresi kazanarak potansiyelini somutlaştırma fırsatı sunabilir.",
     "Damallsvenskan'ın küresel scout trafiği, oyuncunun Avrupa piyasasına erken dahil olmasını kolaylaştırır."],
    ["BK Häcken'deki uzun süreli yedeklik, kaleciler için kritik olan refleks keskinliğini olumsuz etkiler.",
     "Uzun maçsız dönem, ilk forma şansında özgüven eksikliği ve hata yapma riskini artırabilir.",
     "İzlanda'nın küçük futbol ekosistemi, kariyer seçeneklerini kısıtlayabilir."]
),

"Shukurath Oladipo": sw(
    ["Merkez defans (D C) pozisyonunda AS Roma gibi Serie A Femminile'nin en prestijli kulüplerinden birinde bulunması, taktiksel gelişim için üst düzey bir ortama sahip olduğunu kanıtlar.",
     "62/100 FM26 notu ve Nijeryalı bir oyuncu olarak İtalya'da forma mücadelesi vermesi, uluslararası adaptasyon kapasitesini ve mesleki kararlılığını ortaya koymaktadır.",
     "Roma'nın uluslararası marka değeri ve Avrupa kupalarındaki varlığı, oyuncunun küresel scout ağlarına erken dönemde dahil olmasını sağlıyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Serie A'nın zorlu fiziksel ve taktiksel rekabetine hazırlıksız girme riski, performans düşüklüğüne zemin hazırlayabilir.",
     "İstatistiklerin sıfırda olması, savunma etkinliği ve geriden oyun kurma kalitesini analiz etmeyi güçleştiriyor."],
    ["Nijerya Milli Takımı'nın Afrika platformunda güçlü bir stoper adayı olarak değerlendirilebilir.",
     "Roma'dan kiralık bir transfer, düzenli maç süresi kazanarak 62'lik potansiyelini somutlaştırma fırsatı sunabilir.",
     "Serie A'nın yüksek standartlarında çalışmak, uzun vadede kariyer değerini artırabilir."],
    ["Roma'nın derin savunma kadrosu, forma alma sürecini ciddi ölçüde zorlaştırmaktadır.",
     "İtalya'nın yabancı uyruklu oyunculara yönelik rekabet ortamı, kota kısıtlamalarıyla birleşince ek engeller yaratabilir.",
     "Uzun maçsız dönem, stoper pozisyonunda kritik olan savunma koordinasyonunu olumsuz etkiler."]
),

"Mana Lamine": sw(
    ["Sağ açık hücumcu ve santrafor (AM R, ST C) pozisyonlarındaki ikili yetkinlik, bonservis gerektirmeksizin hücum hattına anında kanat–merkez tehdidi kazandırma kapasitesi sunuyor.",
     "Kamerun futbol ekolünden gelen fiziksel güç ve patlayıcı hız, sağ kanat ve santrafor pozisyonlarında rakip savunmalara ciddi meydan okuma fırsatı yaratır.",
     "62/100 FM26 notu, serbest oyuncu statüsüne karşın hücum kapasitesinin değer taşıdığını ve yatırım potansiyeli açısından cazip olduğunu gösteriyor."],
    ["Serbest oyuncu statüsü, herhangi bir takım sisteminden uzak kalmaktan kaynaklanan ritim ve kondisyon kaybı riskini beraberinde getirir.",
     "Bu sezon resmi maçta süre alamamış olması, aktif form ve sahaya hazırlık düzeyini değerlendirmeyi güçleştiriyor.",
     "İstatistiklerin sıfırda olması, hücum pozisyonlarında beklenen gol ve asist üretimini analiz etmeyi olanaksız kılıyor."],
    ["Bonservis bedelsiz transfer edilebilmesi, bütçe kısıtlaması olan kulüpler için maliyet etkin bir hücum çözümü sunuyor.",
     "Kamerun Milli Takımı platformu, Afrika Kupası gibi büyük turnuvalarda uluslararası görünürlük kazanma fırsatı sunuyor.",
     "Sağ kanat ve santrafor kombinasyonu, farklı hücum sistemleri için kolayca uyarlanabilir bir profil oluşturuyor."],
    ["Uzun süre takım sisteminden uzak kalmak, hücum oyuncularında kritik olan ritim, zamanlama ve koordinasyonu olumsuz etkiler.",
     "Kamerun'un Avrupa scout ağlarına sınırlı erişimi, transfer fırsatlarının gecikmesine zemin hazırlayabilir.",
     "Serbest oyuncu durumunun yarattığı kötümser algı, potansiyelinin altında teklifler almasına neden olabilir."]
),

"Melina Reuter": sw(
    ["Sağ orta ve sağ/sol hücum sahası ile santrafor (M R, AM RL, ST C) pozisyonlarındaki geniş çok yönlülük, Carl Zeiss Jena'nın hücumunda birden fazla aksiyona katkı sunuyor.",
     "60/100 FM26 notu, 2. Bundesliga ortamında hücum yelpazesinin geniş tutulduğu yaratıcı bir profil sergilediğini gösteriyor.",
     "Almanya futbol ekolünden gelmesi, pressing anlayışı ve topsuz koşu disiplini konusunda güçlü bir temel sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücum istatistiklerinin sıfırda olması, gol üretimi ve bitiricilik konusundaki etkinliği analiz etmeyi olanaksız kılıyor.",
     "Çok sayıda pozisyondaki esneklik, belirli bir uzmanlık alanının oluşmamasına yol açabilir."],
    ["2. Bundesliga platformu, Bundesliga kulüplerinin scout ağlarına dahil olmak için uygun bir fırsat sunuyor.",
     "Almanya Milli Takımı altyapısı için hücum yelpazesi geniş bir alternatif olarak değerlendirilebilir.",
     "Jena'da düzenli maç süresi yakalandığında, çok yönlü hücum profiliyle scout ilgisini hızla çekebilir."],
    ["Almanya'nın derin hücum oyuncu stoku, üst ligde öne çıkmayı istatistiksel kanıt olmaksızın güçleştiriyor.",
     "Uzun maçsız dönem, hücum oyuncularında kritik olan patlayıcı koşu ve bitiricilik kapasitesini olumsuz etkiler.",
     "Jena'nın görece düşük medya profili, scout ilgisinin gecikmesine zemin hazırlayabilir."]
),

"Ellie Gilbert": sw(
    ["Defansif ve merkez orta saha (DM, M C) pozisyonlarındaki yetkinlik, DC Power FC'nin orta sahasında hem savunma filtresi hem oyun inşası sağlayan değerli bir profil sunuyor.",
     "60/100 FM26 notu, NWSL ortamında top kazanma ve oyun kurma dengesi açısından makul kariyer değeri taşıdığını gösteriyor.",
     "ABD'nin gelişen kadın futbolu altyapısı ve NWSL'in artan küresel görünürlüğü, oyuncunun keşfedilme şansını artırıyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "İstatistiklerin sıfırda olması, pas kalitesi ve top kazanma etkinliğini analiz etmeyi olanaksız kılıyor.",
     "DC Power FC'nin görece düşük medya profili, scout ilgisinin gecikmesine zemin hazırlıyor."],
    ["NWSL'de alacağı düzenli maç süresi, 60'lık potansiyelini somutlaştırarak kariyer değerini artırabilir.",
     "ABD Milli Takımı altyapısı için orta saha alternatifi olarak değerlendirilebilir.",
     "NWSL'in artan uluslararası ilgisi, oyuncunun Avrupa piyasasına erken dönemde dahil olmasını kolaylaştırır."],
    ["NWSL'in Avrupa büyük liglerinden taktiksel olarak ayrışması, üst liga transferinde adaptasyon güçlükleri yaratabilir.",
     "Uzun maçsız dönem, orta saha oyuncularında kritik olan ritim ve tepki hızını olumsuz etkiler.",
     "DC Power FC'nin düşük profili, oyuncunun kariyer hedeflerini gerçekleştirmesi için ek görünürlük gerektiriyor."]
),

"Manon Le Page": sw(
    ["Strasbourg'da D1 Féminine standardında kaleci pozisyonunda görev alması, Fransız kaleci ekolünün teknik eğitimine maruz kaldığını ve gelişim için uygun bir ortamda bulunduğunu gösteriyor.",
     "60/100 FM26 notu, Fransa'nın rekabetçi kaleci havuzunda makul kariyer değeri taşıdığını ve gelişime açık bir profil çizdiğini ortaya koyuyor.",
     "Strasbourg'un D1 Féminine'deki aktif rekabeti, oyuncuya yüksek baskılı ortamlarda gelişim fırsatı sunmaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, maç ritmi ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Strasbourg'daki kaleci rekabetinin yoğunluğu, forma almasını uzun vadede zorlaştırabilir.",
     "İstatistiklerin sıfırda olması, kaleci performansını nesnel olarak değerlendirmeyi güçleştiriyor."],
    ["D1 Féminine'nin aktif scout trafiği, oyuncunun Fransa'nın kaleci piyasasına erken dahil olmasını kolaylaştırır.",
     "Strasbourg'dan kiralık bir transfer, düzenli maç süresi kazanarak potansiyelini somutlaştırma fırsatı sunabilir.",
     "Fransa Milli Takımı altyapısı için kaleci alternatifi olarak değerlendirilebilir."],
    ["D1 Féminine'nin rekabetçi kaleci kadrosu, forma alma sürecini uzatabilir.",
     "Uzun maçsız dönem, kaleciler için kritik olan refleks ve zamanlama konusunda gerileme riski taşır.",
     "Strasbourg'daki yoğun rekabet, oyuncunun motivasyonunu ve gelişim ivmesini olumsuz etkileyebilir."]
),

"Sofia Määttä": sw(
    ["Sol ve sağ orta/ofansif orta saha (M/AM RL) pozisyonlarındaki ikili kanat yetkinliği, Glasgow City'nin kanadında çift yönlü tehdit oluşturma kapasitesi sunuyor.",
     "59/100 FM26 notu, Finlandiya futbol ekolünden gelen disiplinli yapı ve SWPL rekabetinde makul kariyer değeri taşıdığını gösteriyor.",
     "Glasgow City'nin İskoçya'daki dominant konumu ve UEFA Kadın Şampiyonlar Ligi deneyimi, oyuncuya uluslararası kariyer fırsatları sunuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "İstatistiklerin sıfırda olması, kanat pozisyonlarında beklenen hücum katkısını analiz etmeyi olanaksız kılıyor.",
     "SWPL'in Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, üst liga transferinde adaptasyon güçlükleri yaratabilir."],
    ["Glasgow City'nin UEFA Kadın Şampiyonlar Ligi platformu, uluslararası görünürlük kazanmak için değerli bir vitrin sunuyor.",
     "Finlandiya Milli Takımı'nın kanat ihtiyacı, ulusal kariyer kapısını zorlama fırsatı sunuyor.",
     "İkili kanat esnekliği, farklı taktik sistemler kullanan kulüpler için cazip bir transfer profili oluşturuyor."],
    ["SWPL'den daha rekabetçi liglere geçişte adaptasyon güçlükleri yaşanabilir.",
     "Uzun maçsız dönem, kanat oyuncularında kritik olan patlayıcı koşu kapasitesini olumsuz etkiler.",
     "Glasgow City'nin yoğun kanat rekabeti, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir."]
),

"Savanna Duffy": sw(
    ["Kolbotn'da Norveç liginin kaleci pozisyonunda görev alması, İskandinav kaleciliğinin güçlü teknik altyapısına maruz kaldığını gösteriyor.",
     "57/100 FM26 notu, Norveç'in rekabetçi kaleci havuzunda kariyer yolculuğunun başında olan bir profil ortaya koyuyor.",
     "Kolbotn'un Norveç ligindeki köklü yapısı, taktiksel disiplin ve gelişim için uygun bir ortam sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, maç ritmi ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "57'lik FM26 notu, üst liglerle rekabette daha fazla gelişime ihtiyaç duyulduğunu gösteriyor.",
     "Fiziksel verilerinin bilinmemesi, uzun çıkışlar ve hava topu hakimiyeti konusunda belirsizlik yaratıyor."],
    ["Norveç liginde düzenli maç süresi kazanarak gelişim ivmesini artırabilir.",
     "Kolbotn'un Norveç ligindeki aktif varlığı, ilerleyen dönemde daha güçlü kulüplere transfer kapısını aralayabilir.",
     "Erken kariyer döneminde şans bulması, uzun vadeli büyüme için sağlam bir zemin oluşturabilir."],
    ["57'lik FM26 notu, üst liglerdeki rekabetçi kaleci kadroları karşısında forma alma şansını ciddi ölçüde sınırlamaktadır.",
     "Uzun maçsız dönem, kaleciler için kritik olan refleks ve zamanlama konusunda gerileme riski taşır.",
     "Norveç liginin derin kaleci stoku, oyuncunun düzenli forma almasını zorlaştırabilir."]
),

"Carina Wik Alfredsen": sw(
    ["Defansif ve merkez orta saha (DM, M C) pozisyonlarındaki yetkinlik, LSK'nın orta sahasında hem savunma filtresi hem oyun inşası sağlayan bir profil sunuyor.",
     "57/100 FM26 notu, Norveç liginde orta saha kontrolcüsü rolünde gelişim sürecinde olan kariyer yolculuğunu temsil ediyor.",
     "LSK'nın Norveç ligindeki köklü yapısı, taktiksel disiplin ve rekabet odaklı gelişim ortamı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "57'lik FM26 notu, üst liglerle rekabette daha fazla gelişime ihtiyaç duyulduğunu gösteriyor.",
     "İstatistiklerin sıfırda olması, pas kalitesi ve top kazanma etkinliğini analiz etmeyi olanaksız kılıyor."],
    ["LSK'da düzenli maç süresi kazanarak gelişim ivmesini artırabilir.",
     "Norveç liginin İskandinav futbolundaki prestiji, gelecekteki keşfedilme şansını desteklemektedir.",
     "DM–M ikili profili, farklı taktik sistemler için uyarlanabilir bir yapı sunuyor."],
    ["57'lik FM26 notu, üst liglerdeki rekabetçi orta saha kadroları karşısında öne çıkmayı zorlaştırıyor.",
     "Uzun maçsız dönem, orta saha oyuncularında kritik olan ritim ve tepki hızını olumsuz etkiler.",
     "LSK'nın orta saha rekabeti, düzenli forma almasını zorlaştırabilir."]
),

"Liu Yanqiu": sw(
    ["Sağ/sol bek, kanat bek, orta ve ofansif orta saha (D/WB/M/AM RL) genelindeki istisnai çok yönlülük, Jianghan Üniversitesi FC'de her iki koridorda geniş bir yelpazede görev yapma kapasitesi sunuyor.",
     "55/100 FM26 notu, Çin futbol ekolünden gelen adaptasyon kapasitesi ve çok yönlü koridor profiliyle kariyer değeri taşıdığını gösteriyor.",
     "Çin kadın futbolunun son yıllardaki uluslararası yükselişi ve 2023 Dünya Kupası katılımı, oyuncunun daha geniş bir scout ağına dahil olmasını kolaylaştırmaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "Çin liginin Avrupa büyük ligleriyle fiziksel ve taktiksel farkı, üst liga transferinde ciddi adaptasyon güçlükleri yaratabilir.",
     "İstatistiklerin sıfırda olması, kanat ve orta sahada beklenen katkıyı analiz etmeyi olanaksız kılıyor."],
    ["Çin Milli Takımı'nın çift koridorlu esnekliğe ihtiyaç duyduğu dönemlerde ulusal kariyer kapısını zorlayabilir.",
     "NWSL, WSL veya J1 Women League gibi liglere yönelik bir transfer, Çin liginin ötesinde kariyer ivmesini artırabilir.",
     "Çok yönlü koridor profili, farklı taktik sistemler kullanan kulüpler için düşük maliyetli bir transfer hedefi oluşturuyor."],
    ["Çin'in Avrupa scout ağlarına sınırlı erişimi, transfer fırsatlarının gecikmesine zemin hazırlayabilir.",
     "55'lik FM26 notu, üst liglerle rekabette öne çıkmak için daha fazla gelişime ihtiyaç duyulduğunu gösteriyor.",
     "Uzun maçsız dönem, çok sayıda pozisyonu sürdüren oyuncuda kas ve koordinasyon düzeyinde gerilemeye yol açabilir."]
),

"Jasmin Mansaray": sw(
    ["Sağ ve merkez bek (D RC) pozisyonlarındaki ikili yetkinlik, LSK'nın savunma hattında sağ aksın her iki rolünü karşılama kapasitesi sunuyor.",
     "53/100 FM26 notu, Finlandiya futbol ekolünden gelen güçlü savunma disiplini ve mücadele azmiyle kariyer yolculuğunun başında olan bir profil ortaya koyuyor.",
     "LSK'nın Norveç ligindeki köklü yapısı, taktiksel disiplin ve rekabet odaklı gelişim ortamı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "53'lük FM26 notu, üst liglerle rekabette daha fazla gelişime ihtiyaç duyulduğunu açıkça gösteriyor.",
     "İstatistiklerin sıfırda olması, savunma etkinliği ve geriden oyun açma kalitesini analiz etmeyi olanaksız kılıyor."],
    ["LSK'da düzenli maç süresi kazanarak hem teknik hem de fiziksel gelişim ivmesini artırabilir.",
     "Finlandiya Milli Takımı'nın genç savunma kadrosu için uzun vadeli bir aday olarak değerlendirilebilir.",
     "Norveç liginin rekabetçi yapısı, oyuncuya zorlu koşullarda gelişim fırsatı sunuyor."],
    ["53'lük FM26 notu, üst liglerdeki rekabetçi savunma kadroları karşısında ciddi bir engel oluşturmaktadır.",
     "Uzun maçsız dönem, stoper pozisyonunda kritik olan savunma koordinasyonunu olumsuz etkiler.",
     "LSK'nın savunma rekabeti, düzenli forma almasını zorlaştırarak gelişim ivmesini yavaşlatabilir."]
),

"Jo-Anne Conquist": sw(
    ["Merkez bek ve defansif orta saha (D C, DM) pozisyonlarındaki ikili yetkinlik, FC Rosengård'ın savunma hattında hem stoper hem orta saha köprüsü rolünü üstlenme kapasitesi sunuyor.",
     "52/100 FM26 notu, İsveç Damallsvenskan'ın rekabetçi ortamında kariyer yolculuğunun başında olan bir savunma profilini temsil ediyor.",
     "FC Rosengård'ın Damallsvenskan'daki ve UEFA Kadın Şampiyonlar Ligi'ndeki prestijli konumu, gelişim için üst düzey bir rekabet ortamı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "52'lik FM26 notu, gelişim yolculuğunun henüz başında olduğunu ve üst liglerle rekabette daha fazla çalışma gerektirdiğini gösteriyor.",
     "İstatistiklerin sıfırda olması, savunma etkinliği ve DM rolündeki oyun kurma kalitesini analiz etmeyi güçleştiriyor."],
    ["Rosengård'ın Şampiyonlar Ligi platformu, uluslararası görünürlük kazanmak için paha biçilmez bir fırsat sunuyor.",
     "İsveç Milli Takımı'nın uzun vadeli savunma planlaması için genç bir aday olarak değerlendirilebilir.",
     "Stoper–DM ikili profili, farklı savunma sistemleri kullanan kulüpler için uyarlanabilir bir transfer profili oluşturuyor."],
    ["52'lik FM26 notu ve Rosengård'ın derin savunma kadrosu, forma alma şansını ciddi ölçüde sınırlıyor.",
     "Uzun maçsız dönem, stoper ve DM pozisyonlarında kritik olan otomatizmi olumsuz etkiler.",
     "Yüksek beklenti ortamında yetersiz maç deneyimiyle baskıya maruz kalmak, kariyer güvenini olumsuz etkileyebilir."]
),

"Carolina Pimenta": sw(
    ["Sağ/sol/merkez bek, sağ/sol kanat bek ve merkez orta saha (D RLC, WB RL, M C) genelindeki istisnai çok yönlülük, Sporting CP B için savunma ve orta saha hattında kapsamlı seçenekler sunuyor.",
     "52/100 FM26 notu, Portekiz'in köklü kulübü Sporting CP altyapısında yetişen ve kariyer yolculuğunun başında olan geniş yelpazeli bir profil ortaya koyuyor.",
     "Sporting CP'nin Portekiz ve Avrupa futbolundaki güçlü marka değeri, oyuncuya üst düzey bir gelişim ve tanınma ortamı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, form ve kondisyon konusundaki değerlendirmeyi güçleştirmektedir.",
     "52'lik FM26 notu, gelişim sürecinin henüz başında olduğunu gösteriyor ve üst liglerle rekabette önemli bir açığın kapanması gerektiğine işaret ediyor.",
     "Bu denli geniş pozisyon yelpazesi, belirli bir uzmanlık alanının oluşmamasına yol açabilir."],
    ["Sporting CP'nin Portekiz ligindeki ve Avrupa kupalarındaki varlığı, scout görünürlüğü için değerli bir platform sunuyor.",
     "Portekiz Milli Takımı'nın uzun vadeli kadro planlaması için uyarlanabilir bir savunma profili olarak değerlendirilebilir.",
     "Çok yönlü koridor ve orta saha profili, farklı taktik sistemler kullanan kulüpler için düşük maliyetli bir transfer hedefi oluşturuyor."],
    ["52'lik FM26 notu ve Sporting CP'nin güçlü kadrosu, A takımına geçişi ve düzenli forma almayı zorlaştırıyor.",
     "Uzun maçsız dönem, bu kadar geniş pozisyon yelpazesini sürdüren oyuncuda kas ve koordinasyon düzeyinde gerilemeye yol açabilir.",
     "Portekiz'in Avrupa scout ağlarına sınırlı erişimi, transfer fırsatlarının gecikmesine zemin hazırlayabilir."]
),

"Magdalena Sobal": sw(
    ["Klasik santrafor (ST C) pozisyonunda Juventus gibi Serie A Femminile'nin en prestijli kulüplerinden birinde bulunması, gol bölgesinde İtalyan liginin üst düzey savunmalarıyla çalışma fırsatı sunuyor.",
     "51/100 FM26 notu, kariyer yolculuğunun başında olan Polonyalı bir santrafor profilini temsil etmekte ve gelişim potansiyeline işaret etmektedir.",
     "Juventus altyapısının sağladığı bireysel gelişim programları ve elit antrenör kadrosu, teknik ve taktiksel büyüme için değerli bir ortam oluşturuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, gol üretimi ve maç kondisyonu konusundaki değerlendirmeyi güçleştirmektedir.",
     "51'lik FM26 notu, Serie A seviyesinde rekabet edebilmek için önemli bir gelişim sürecinin gerektiğini gösteriyor.",
     "Juventus'taki yoğun hücum rekabeti, forma alma sürecini uzun vadede zorlaştırmaktadır."],
    ["Juventus altyapısından geçmenin sağladığı teknik birikim, gelecekte daha rekabetçi bir profile sahip olmayı destekler.",
     "Polonya Milli Takımı'nın santrafor kadrosunda uzun vadeli bir alternatif olarak değerlendirilebilir.",
     "Juventus'tan kiralık bir transfer, düzenli maç süresi kazanarak potansiyelini geliştirme fırsatı sunabilir."],
    ["51'lik FM26 notu, Juventus seviyesinin gerisinde kalmayı ve uzun vadeli yedeklik riskini beraberinde getiriyor.",
     "Serie A'nın zorlu savunma anlayışı, santrafor pozisyonunda teknik eksiklikleri hızla gün yüzüne çıkarabilir.",
     "Juventus'ta uzun süre yedek kalmak, kariyer gelişimi için kritik olan maç deneyiminden yoksun kalma riskini barındırır."]
),

"Angel Gurhem": sw(
    ["Sol orta saha (M L) pozisyonunda Fransa ekolünden gelen taktiksel disiplin ve bonservis bedelsiz transfer edilebilirlik, bütçe kısıtlaması olan kulüpler için pratik bir sol saha çözümü sunuyor.",
     "50/100 FM26 notu, kariyer yolculuğunun başında olan ve gelişime açık bir Fransız sol saha profili ortaya koymaktadır.",
     "Serbest oyuncu statüsü, farklı takım sistemlerine hızlıca adapte olarak değer gösterme konusunda esneklik sağlamaktadır."],
    ["Serbest oyuncu statüsü, herhangi bir takım sisteminden uzak kalmaktan kaynaklanan ritim ve kondisyon kaybı riskini beraberinde getirir.",
     "50'lik FM26 notu, üst liglerle rekabette önemli bir gelişim açığının bulunduğunu açıkça gösteriyor.",
     "İstatistiklerin sıfırda olması, sol saha pozisyonunda beklenen katkıyı analiz etmeyi olanaksız kılıyor."],
    ["Bonservis bedelsiz transfer edilebilmesi, Fransa'nın D2 Féminine veya başka liglerin küçük bütçeli kulüpleri için pratik bir seçenek oluşturuyor.",
     "Doğru bir çalışma ortamı ve sistematik gelişim planıyla, 50'lik potansiyelin ötesine geçen kariyer ivmesi kazanabilir.",
     "Sol saha pozisyonundaki profil, kadro derinliği arayan kulüpler için düşük riskli bir tercih oluşturuyor."],
    ["50'lik FM26 notu, orta ve üst seviye liglerde rekabetçi bir ilk 11 yeri için önemli bir engel oluşturmaktadır.",
     "Serbest oyuncu durumunun yarattığı olumsuz algı, olası transfer tekliflerinin düşük tutulmasına neden olabilir.",
     "Uzun süreli takımsız kalma, forma dönüşünde ciddi kondisyon ve özgüven eksikliği yaratabilir."]
),
}

# Load JSON
with open("data/hidden_gems.json", "r", encoding="utf-8") as f:
    players = json.load(f)

patched = 0
for p in players:
    name = p.get("name", "")
    if name in SWOTS and "swot" not in p:
        p["swot"] = SWOTS[name]
        patched += 1

with open("data/hidden_gems.json", "w", encoding="utf-8") as f:
    json.dump(players, f, ensure_ascii=False, indent=2)

print(f"Part 2 done: {patched} SWOTs patched into data/hidden_gems.json")
