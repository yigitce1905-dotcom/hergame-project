# patch_swots_part1.py  — Players 15-57 (first half of missing SWOTs)
# Run from project root: python scripts/patch_swots_part1.py
import json, datetime

TS = "2026-05-27T15:00:00.000000+00:00"
MODEL = "claude-sonnet-4-5"

def sw(s, w, o, t):
    return {"strengths": s, "weaknesses": w, "opportunities": o, "threats": t,
            "generated_at": TS, "model": MODEL}

SWOTS = {
"Annaëlle Tchakounté": sw(
    ["80/100 FM26 scout notu, merkez savunmada elit düzey pozisyon bilgisi ve agresif kapma refleksleri olduğunu kanıtlıyor.",
     "Fransa altyapı ekolünden yetişmesi sayesinde yüksek taktiksel disipline ve dar alanda top sahibi olma becerisine sahiptir.",
     "Strasbourg'da genç bir savunmacı olarak edindiği D1 Féminine deneyimi, baskı altında soğukkanlı karar verme kapasitesini güçlendirmektedir."],
    ["Mevcut sezonda resmi maç istatistiklerinin sıfır olması, maç kondisyonu ve oyun ritmi eksikliğine işaret etmektedir.",
     "Merkez stoper dışındaki pozisyonlarda oynama deneyiminin sınırlı olması, teknik direktörün taktik esnekliğini kısıtlayabilir.",
     "Fiziksel ve demografik verilerinin belirsizliği, hava topu mücadelelerindeki etkinliği hakkında soru işaretleri doğurmaktadır."],
    ["D1 Féminine platformu, daha büyük bütçeli Avrupa kulüplerinin radarına girebilmek için ideal bir vitrin sunmaktadır.",
     "Fransa Milli Takımı'nın genç savunma kuşağına dahil olarak uluslararası kariyer yolunu açabilir.",
     "Doğru bir gelişim planıyla, Strasbourg'un iddialı savunma sisteminin temel taşlarından biri haline gelebilir."],
    ["Süre alamamaya devam etmesi, 80'lik potansiyelin körelmesine ve piyasa değerinin hızla düşmesine yol açabilir.",
     "Savunma hattında kendisinden daha deneyimli rakiplerin varlığı, forma almasını uzun vadede zorlaştırabilir.",
     "Maç eksiğinin yarattığı özgüven bunalımı, ilk şans geldiğinde hata yapma riskini artırabilir."]
),

"Lilli Purtscheller": sw(
    ["Sağ kanat orta saha (M/AM R) pozisyonunda yüksek hız ve teknik geçiş kapasitesine sahip olması, hücum aksiyonlarında belirleyici rol oynamasını sağlar.",
     "80/100 FM26 puanı ve SGS Essen gibi Bundesliga standardındaki bir kulüpte oynaması, elit seviyede rekabete hazır olduğunu gösterir.",
     "Avusturya futbol ekolünün fiziksel disipliniyle Alman liginin tempolu yapısını harmanlayan çok yönlü bir kanatlı profil çiziyor."],
    ["0 maç ve 0 katkı istatistiği, bu sezon henüz forma alamamış olduğunu ve ciddi bir maç ritmi eksikliği yaşadığını ortaya koymaktadır.",
     "Savunmaya dönüş ve ikinci bölgedeki pressing katkısı konusunda ofansif ağırlıklı profilinden kaynaklanan soru işaretleri mevcuttur.",
     "Tercih edilen ayak bilgisinin belirsizliği, özellikle kanatlarda pas açısı ve çapraz top tercihleri hakkında analizi zorlaştırır."],
    ["Bundesliga platformu, İngiltere ve İspanya gibi daha büyük piyasaların transfer radarlarına girmek için güçlü bir fırsat sunmaktadır.",
     "Avusturya Milli Takımı'nın kanat pozisyonunda ihtiyaç duyduğu yaratıcı profil, ona uluslararası düzeyde düzenli süre şansı verebilir.",
     "SGS Essen'in genç yeteneklere verdiği fırsatlar, sezonun ilerleyen döneminde ilk 11'e girme şansını artırabilir."],
    ["Almanya'nın yüksek tempolu ve fiziksel rekabet ortamında süre alamamak, oyuncunun gelişim ivmesini ciddi şekilde yavaşlatabilir.",
     "Avusturya ligine kıyasla daha sert olan Bundesliga defans baskısına uyum sağlamak ilk etapta performansını olumsuz etkileyebilir.",
     "Rakip kanatlı oyuncuların yüksek rekabeti karşısında formayı kapmak için gereken uyum süreci beklentilerin altında kalabilir."]
),

"Holly Ward": sw(
    ["Hem sağ açık hücumcu hem de santrafor (AM R, ST C) olarak oynayabilmesi, hücum hattında çok boyutlu bir tehdit oluşturma kapasitesi sağlar.",
     "79/100 FM26 scout notu, Kanada futbol ekolünden gelen güçlü atletizm ve yüksek hücum zekasıyla desteklenmektedir.",
     "Vancouver Rise'da NWSL liginin rekabetçi yapısında forma giymesi, fiziksel ve zihinsel olarak en üst seviyeye hazır olduğunu gösterir."],
    ["Bu sezon henüz süre alamamış olması, maç kondisyonu ve oyun içi ritim açısından önemli bir eksiklik oluşturmaktadır.",
     "0 gol ve 0 asist ile bitiricilik ve son pas kalitesi konusundaki etkinliği henüz kanıtlanamamıştır.",
     "Fiziksel parametrelerin bilinmemesi, rakip savuncularla üst düzey fiziksel mücadelelerdeki başarı oranını belirsiz kılmaktadır."],
    ["NWSL'in artan global görünürlüğü, Avrupa kulüplerinin keşfedebileceği ideal bir vitrin sunmaktadır.",
     "Kanada Milli Takımı'nın olimpiyat ve Dünya Kupası döngülerindeki kadro ihtiyacı, onu uluslararası arenaya taşıyabilir.",
     "İkili hücum pozisyonundaki çok yönlülüğü, farklı sistemlerdeki takımlar için kolayca adapte olabilecek cazip bir profil oluşturur."],
    ["Süre eksikliğinin uzaması, özellikle hız gerektiren hücum pozisyonlarında form ve patlayıcılık kaybına neden olabilir.",
     "NWSL'in Avrupa liglerine kıyasla daha az mediatik yapısı, potansiyelinin küresel ölçekte fark edilmesini geciktirebilir.",
     "Santrafor ve kanat arasındaki ikinci planda kalma durumu, teknik direktörün sistemine göre tercih edilmemesi riskini barındırır."]
),

"Fiona Gaißer": sw(
    ["Hem defansif hem de merkez orta saha (DM, M C) pozisyonlarında oynayabilmesi, takımın oyun kontrol gücüne çift yönlü katkı sunar.",
     "Almanya futbol altyapısından çıkmış olması, disiplinli pressing anlayışı ve top kazanma verimliliği konusunda güçlü bir temel sağlar.",
     "79/100 FM26 notu, Carl Zeiss Jena'da 2. Bundesliga rekabetinde kendini ispat etmiş genç bir orta saha profili ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, maç ritmi ve anlık karar verme hızı açısından ciddi bir eksikliği işaret etmektedir.",
     "Hücuma katkı istatistiklerinin sıfırda kalması, top kazanmanın ötesinde oyun kurma ve skor üretme konusunda gelişime ihtiyaç olduğunu gösteriyor.",
     "Fiziksel veri eksikliği, zorlu mücadelelerde üst vücut kuvveti ve hava topu başarı oranı hakkında belirsizlik yaratmaktadır."],
    ["2. Bundesliga'nın Alman futbolunun kapısını aralayan yapısı, daha büyük liglere geçiş için erken kariyer adımı atmaya imkân verir.",
     "Almanya Milli Takımı'nın genç orta saha havuzuna dahil olarak uluslararası kariyer kapısını zorlama şansı yüksektir.",
     "İkili orta saha pozisyonundaki esnekliği, takım içindeki ilk 11 mücadelesinde ona rekabetçi avantaj sağlar."],
    ["Maç eksiğinin yarattığı gelişim durağanlığı, Almanya'nın rekabetçi orta saha ekibinde geri planda kalma riskini beraberinde getirir.",
     "İkinci ligdeki kalıpların ve oyun temposunun sınırları, Bundesliga seviyesine geçişte adaptasyon sorunlarına yol açabilir.",
     "Genç yaşta yaşanacak olası bir sakatlık, 79'luk yüksek potansiyelini gerçeğe dönüştürme sürecini sekteye uğratabilir."]
),

"Elin Sørum": sw(
    ["Stoper, defansif orta saha ve merkez orta saha (D C, DM, M/AM C) olarak oynanabilen istisnai çok yönlülük, teknik direktöre geniş taktiksel seçenekler sunar.",
     "Rosenborg gibi Norveç kadın futbolunun güçlü kulübünde edindiği deneyim, hem savunma hem orta saha kurgusunda olgunluk sağlamıştır.",
     "78/100 FM26 puanı, farklı pozisyonlardaki bu esnekliğin yüksek teknik kapasite ve oyun okumayla desteklendiğini kanıtlar."],
    ["Resmi maç istatistiklerinin sıfır olması, oyuncunun bu sezon aktif rekabetten uzak kaldığını göstermektedir.",
     "Çok yönlülüğünün getirdiği rol belirsizliği, en verimli olduğu ana pozisyonun net olarak belirlenmesini zorlaştırabilir.",
     "Sahada katkısını somutlaştıracak gol ve asist verilerinin bulunmaması, son bölgedeki etkisini ölçmeyi güçleştirmektedir."],
    ["Üç ayrı pozisyonda oynayabilmesi, kadrosunda derinlik arayan büyük Avrupa kulüplerinin transfer listesine girebilmesini kolaylaştırır.",
     "Norveç Milli Takımı'na seçilmek ve Şampiyonlar Ligi gibi vitrin platformlarda oynamak için uygun bir profil çizmektedir.",
     "Rosenborg'un Norveç ligindeki dominant konumu, oyuncunun gelişimini hızlandıracak kaliteli antreman ve maç ortamı sunar."],
    ["Bir pozisyona odaklanamamak, üst düzey kulüplerde spesifik bir role ihtiyaç duyulduğunda tercih dışı kalmasına neden olabilir.",
     "Maç oynama fırsatı bulamadığı sürenin uzaması, çok yönlü profilinin herhangi bir alanda körelmesine yol açabilir.",
     "Norveç ligi ile Avrupa'nın büyük ligleri arasındaki rekabet ve fiziksel fark, olası erken bir transferde adaptasyonu zorlaştırabilir."]
),

"Elise Thorsnes": sw(
    ["Hem stoper hem de santrafor (D C, ST C) olarak oynayabilmesi, modern futbolun talep ettiği nadir çift yönlü çok yönlülüğü temsil etmektedir.",
     "Vålerenga'da üst düzey Norveç ligi deneyimi kazanması, hem savunma hem hücum faslında oyun okumasını güçlü kılmaktadır.",
     "78/100 FM26 puanı, iki kritik pozisyondaki teknik kapasitesinin scout değerlendirmelerinde üst sıralarda yer bulduğunu kanıtlar."],
    ["Bu sezon resmi maç oynamamış olması, oyuncunun mevcut fiziksel durumu ve form grafiği hakkında ciddi soru işaretleri doğurmaktadır.",
     "Savunma ve hücum arasındaki pozisyon ikiliği, rolünün net tanımlanmaması durumunda takım içi uyumda karmaşa yaratabilir.",
     "İstatistik verilerinin tamamen sıfırda olması, hangi pozisyonda daha etkili olduğunun analitik olarak değerlendirilmesini imkânsız kılmaktadır."],
    ["Stoper–santrafor çift yönlülüğü, uzun dönemli kademelendirme yapan büyük kulüplerin dikkatini kolayca çekebilir.",
     "Norveç Milli Takımı'nın hem savunma hem hücumda kadro sıkıntısı yaşadığı anlarda ona yerinde çözüm üretme şansı doğabilir.",
     "İyi bir performans serisinin ardından, İskandinav pazarının ötesine uzanan bir transfer penceresini zorlayabilir."],
    ["Pozisyon belirsizliği, teknik direktörlerin oyuncuyu planlarına dahil ederken kararsız kalmasına neden olabilir.",
     "Uzun süreli maçsız kalma, yeniden sahaya dönerken hem kondisyon hem özgüven konusunda ciddi bir baskı oluşturabilir.",
     "Norveç liginin Avrupa değerlendirmesindeki görece sınırlı ağırlığı, potansiyelinin geniş kitleler tarafından fark edilmesini geciktirebilir."]
),

"Beke Sterner": sw(
    ["Sağ bek ve kanat bek (D/WB R) pozisyonlarındaki esneklik, özellikle 3-4-3 ve 4-3-3 gibi kanat ağırlıklı sistemlerde teknik direktöre kritik seçenekler sunar.",
     "Almanya Bundesliga altyapısından gelen SGS Essen formasıyla, üst düzey taktiksel eğitim ve fiziksel rekabet altyapısına sahiptir.",
     "78/100 FM26 puanı, sağ koridor dominansındaki kapasitesiyle Alman kadın futbolunun en umut vadeden beklerinden biri olduğunu tescilliyor."],
    ["Sezon istatistiklerinin tamamının sıfırda olması, maç ritmi ve hücuma katkı açısından önemli eksiklikler taşıdığını göstermektedir.",
     "Kanat bek pozisyonunda birinci bölge geçişleri ve son pas kalitesi konusundaki veriler henüz yetersizdir.",
     "Fiziksel parametrelerinin bilinmemesi, üst düzey forvarlara karşı savunma mücadelelerindeki başarı oranını belirsiz bırakmaktadır."],
    ["SGS Essen'in Bundesliga'daki konumu, onu Almanya'nın gençlik milli takımları için doğal bir talep havuzuna yerleştirmektedir.",
     "Modern futbolun agresif sağ bek profillerine duyduğu yoğun ihtiyaç, daha büyük kulüplerin transfer listelerinde öne çıkmasını kolaylaştırır.",
     "Bundesliga performansını somutlaştıracak maçlar bulduğunda, İspanya ve İngiltere gibi lüks piyasaların radarına girme kapısı açılır."],
    ["Forma alamamaya devam ederse, Alman kadın futbolunun derin kanat bek stoku içinde değer kaybetme riski taşımaktadır.",
     "Bundesliga rekabetinin yüksek temposu, maçsız dönemden sonra aniden içine girildiğinde fiziksel ve taktiksel adaptasyonu zorlaştırır.",
     "Takım içinde kendisinden daha deneyimli rakiplerin varlığı, düzenli ilk 11 şansı bulmasını uzun vadede güçleştirebilir."]
),

"Julie Jorde": sw(
    ["Hem defansif hem de merkez orta saha (DM, M C) rollerinde oynaması, takımın orta saha dengesini her iki yönde sağlama kapasitesi sunuyor.",
     "Brøndby IF gibi Danimarka'nın ve kadın futbolunun Şampiyonlar Ligi tecrübesi olan bir kulübünde forma giymesi elit altyapıya işaret eder.",
     "78/100 FM26 notu, top kazanma verimliliği ve birinci bölge müdahale kapasitesi açısından üst düzey bir profil ortaya koyuyor."],
    ["Bu sezon hiç süre alamamış olması, takım kurgusu içindeki yeri ve fiziksel hazırlık durumu konusunda ciddi belirsizlik yaratmaktadır.",
     "Hücuma katkısının sıfır olması, üçüncü bölge top taşıma ve son pas üretimi konusundaki etkinliğini sorgulatmaktadır.",
     "Norveç kökenli bir oyuncu olarak Danimarka ligi alışkanlıklarına uyum süreci takım içindeki yerleşme sürecini uzatabilir."],
    ["Brøndby'nin UEFA Kadınlar Şampiyonlar Ligi platformu, Scout görünürlüğü açısından paha biçilmez bir fırsat sunmaktadır.",
     "Norveç Milli Takımı kadrosunda orta saha arayışı devam ettiği sürece uluslararası sahne için güçlü bir alternatif konumundadır.",
     "İyi bir form serisi yakaladığında, İskandinav pazarının sınırlarını aşarak Batı Avrupa liglerinin kapısını zorlayabilir."],
    ["Danimarkalı rakiplerle olan kültürel ve oyun anlayışı farklılıkları, takım içi entegrasyonu ve iletişimi olumsuz etkileyebilir.",
     "Uzun süreli yedekliğin devam etmesi, 78'lik potansiyelin körelmesine ve piyasa değerinin gerilemesine zemin hazırlar.",
     "Brøndby'nin orta saha rekabetinin yoğunluğu, oyuncunun forma şansını uzun vadede kısıtlamaya devam edebilir."]
),

"Manon Wahl": sw(
    ["Fransa kaleci okulunun yetiştirdiği bir kaleci olarak, ceza sahası hakimiyeti ve yan toplardaki pozisyon alma becerisi üst düzeydedir.",
     "Strasbourg gibi D1 Féminine'in rekabetçi kulüplerinden birinde görev alması, yüksek baskılı maçlardaki reaksiyon kapasitesini güçlendirmektedir.",
     "78/100 FM26 notu, ayakla oyun kurma ve pres altında pas dağıtma becerilerini içeren modern kaleci profiliyle örtüşmektedir."],
    ["Bu sezon resmi maç oynamamış olması, sahaya döndüğünde zamanlama, refleks ve koordinasyon açısından ciddi adaptasyon gerektireceğini gösterir.",
     "Fiziksel verilerinin bilinmemesi, özellikle uzun pas çıkışlarında ve hava topu müdahalelerindeki etkinlik analizi yapılmasını engeller.",
     "Uzun süreli rekabetten kopukluk, özellikle üst düzey liglerde beklenmedik hata riski ve özgüven bunalımı yaratabilir."],
    ["D1 Féminine'deki düzenli rakip analizleri ve maç video arşivleri, teknik gelişimini hızlandırabilecek zengin bir kaynak sunuyor.",
     "Fransa Milli Takımı kaleci rotasyonuna dahil olma potansiyeli, uluslararası arenada kariyer hedeflerini gerçekleştirme kapısını aralıyor.",
     "Strasbourg'dan yapılacak olası bir kiralama transferi, düzenli maç süresi kazanarak 78'lik potansiyelini sahaya yansıtma imkânı sunar."],
    ["Uzun süre resmi maçtan uzak kalması, rakip kalecilere kıyasla form farkının açılmasına ve kadro tercihlerinde geride kalmasına neden olabilir.",
     "D1 Féminine'in hızla değişen rekabet ekosisteminde süre bulamamak, genç kaleciler için kariyer açısından telafi edilemez kayıplara yol açabilir.",
     "Takımdaki başka bir kaleciyle yaşanacak olası rekabet, forma alamaması durumunda sezon sonu transfer bütçesine yansıyabilecek beklenti düşüklüğüne sebep olur."]
),

"Anna Aahjem": sw(
    ["Klasik santrafor (ST C) profiliyle gol pozisyonu bulma ve ceza sahasında tamamlama reflekslerini ön plana çıkaran ofansif bir oyun stili sergilemektedir.",
     "Brann gibi Norveç'in ve Şampiyonlar Ligi katılımcısı bir kulübünde forma giymesi, elit düzey hücum rekabetine maruz kaldığını gösterir.",
     "78/100 FM26 notu, santraforlar için kritik olan top kilit alma ve kaleyi bulan vuruş kapasitesi açısından üst sıralarda değerlendirildiğine işaret eder."],
    ["Bu sezon resmi maç oynamamış olması, gol bölgesindeki bitiricilik kalitesini ve mevcut form durumunu değerlendirmeyi güçleştirmektedir.",
     "Yalnızca santrafor pozisyonuna odaklanması, taktiksel esneklik açısından kanallar ya da ikinci golcü rolüyle sınırlı bir profil oluşturabilir.",
     "Fiziksel verilerin eksikliği, hava toplarında rakip stoperiyle yaşanacak güç mücadelelerindeki başarı oranını belirsiz kılmaktadır."],
    ["Brann'ın Şampiyonlar Ligi platformu, Avrupa'nın büyük kulüplerinin scouting raporlarına girme şansını önemli ölçüde artırır.",
     "Norveç'te gelişen kadın futbolu ekosistemi ve yükselen yayın ortaklıkları, oyuncunun görünürlüğünü küresel ölçekte genişletmektedir.",
     "İyi bir form yakaladığında daha büyük liglere transfer kapısını açabilecek, hem piyasa değeri hem de kariyer ivmesi açısından güçlü bir profil çiziyor."],
    ["Maç oynayamamanın yarattığı ritim kaybı, yüksek tempolu karşılaşmalarda gol pozisyonlarını dönüştürmede gecikmeye ve etkinlik düşüşüne yol açabilir.",
     "Brann hücum hattındaki rekabet, oyuncunun formayı kazanmasını ve istikrarlı bir süre almasını uzun vadede zorlaştırabilir.",
     "Santraforlara özgü yüksek pozisyon kaybı ve sakatlık riski, özellikle uzun maçsız dönem sonrası forma dönüşlerde ciddi tehlike barındırır."]
),

"Josefine Birkelund": sw(
    ["Hem sağ bek hem de sağ kanat bek (D RC, WB R) pozisyonlarında oynayabilmesi, sağ koridorda hem savunma hem hücum katkısı sunan çift yönlü bir profil çiziyor.",
     "Brann'ın elit rekabet ortamı ve Şampiyonlar Ligi deneyimi, oyuncunun taktiksel disiplin ve yüksek baskı adaptasyon kapasitesini güçlendirmiştir.",
     "77/100 FM26 puanı, kanat bek–bek ikilisindeki teknik kapasitesinin ve gelişim eğrisinin ilerleyen yıllarda daha da yükseleceğini gösteriyor."],
    ["Bu sezon resmi maç süresinin sıfır olması, kondisyon, maç hızı ve takım içi kimya açısından geri planda kaldığını işaret etmektedir.",
     "Hücuma katkı istatistiklerinin bulunmaması, son bölgedeki üretkenlik ve son pas kalitesi konusundaki etkinliği sorgulatmaktadır.",
     "Fiziksel verilerin belirsizliği, birinci bölge topbaşı mücadelelerindeki performans analizini güçleştirmektedir."],
    ["Brann'ın Avrupa platformu, oyuncunun küresel scout ekranlara çıkması için ender bulunan bir fırsat penceresi açmaktadır.",
     "Modern futbolda sağ koridor ağırlıklı sistemlerde sürekli artan kanat bek talebi, transfer piyasasında ona yüksek değer biçilmesini kolaylaştırır.",
     "Norveç Milli Takımı'nın genç kadrosunda hak ettiği yeri aldığında, uluslararası kariyer grafiği hızla yükselebilir."],
    ["Uzun maçsız dönem, kondisyon ve maç içi otomatizm açısından yaşlarına uygun dönemde kritik gelişim boşluğu yaratabilir.",
     "Brann hücum yönelimli savunma sisteminde daha deneyimli rakipler, uzun vadeli kadro rekabetinde öne geçebilir.",
     "Hem savunma hem kanat bek rolünde yarım kalmak, üst düzey transferlerde spesifik pozisyon kriterini karşılamada yetersiz görülmesine neden olabilir."]
),

"Mille Ivi Christensen": sw(
    ["DM ile merkez-ofansif orta saha (DM, M/AM C) arasındaki çift yönlü rol yetkinliği, orta sahada hem kontrol hem yaratıcılık sağlayan nadir bir profil sunuyor.",
     "LSK gibi Norveç kadın futbolunun köklü ve rekabetçi kulüplerinden birinde bulunması, yüksek oyun IQ'su ve taktiksel olgunluk kazandırmaktadır.",
     "77/100 FM26 notu, hem defansif kapama hem de ofansif organizasyondaki verimliliğiyle dengeli bir orta saha kimliği oluşturmaktadır."],
    ["Bu sezon resmi maç süresinin bulunmaması, oyun ritmi ve otomatik tepki hızı açısından eksiklik taşıdığını ortaya koymaktadır.",
     "DM–AM arasındaki pozisyon esnekliği, belirli bir taktik sistemde birincil rol belirsizliğine yol açabilir.",
     "Gol ve asist verilerinin sıfırda olması, hücum katkısının yeterince test edilmediğini göstermektedir."],
    ["Norveç ligi merkezli bu profilin İskandinav takımlarının ötesinde Almanya ve İngiltere gibi liglere transfer yolu açması, çok yönlülüğünden güç almaktadır.",
     "Norveç Milli Takımı'nın orta saha yenilenme sürecinde öne çıkarak uluslararası kariyer basamağını tırmanabilir.",
     "DM ve ofansif pozisyonlarda oynayabilmesi, farklı taktik profil arayan birçok teknik direktör için ideal kadro derinliği kaynağıdır."],
    ["Maçsız geçirilen uzun dönem, özellikle orta sahada gereken hız ve refleks düzeyinin gerileme riskini beraberinde getirir.",
     "LSK'da gençler arasındaki yoğun rekabet, forma alma şansını kısıtlayarak gelişim ivmesini yavaşlatabilir.",
     "İskandinav liglerinin Batı Avrupa'daki temsil gücünün düşüklüğü, uluslararası transfer taleplerinin gecikmesine yol açabilir."]
),

"Synne Aunehaugen": sw(
    ["Merkez stoper (D C) pozisyonunda yüksek pozisyon bilgisi ve ikili mücadele kapasitesi, Rosenborg savunma hattının güvenilir bir üyesi olduğunu ortaya koymaktadır.",
     "77/100 FM26 scout notu, oyuncunun elit düzey bir savunmacı adayı olarak değerlendirildiğini ve gelişim yolculuğunun henüz başladığını gösteriyor.",
     "Rosenborg'un Norveç ligindeki güçlü savunma kültürü, oyuncuya yüksek düzeyli bir taktiksel eğitim ortamı sağlamaktadır."],
    ["Bu sezon henüz resmi maçta süre almamış olması, mevcut kondisyon ve oyun hazırlığı konusunda ciddi soru işaretleri doğurmaktadır.",
     "Istatistiklerin tümüyle sıfırda olması, geriden oyun kurma kalitesi ve ani baskı altındaki tepkiler hakkında değerlendirme yapmayı olanaksız kılmaktadır.",
     "Fiziksel verilerin bilinmemesi, hava topu mücadelelerindeki dominant ya da dezavantajlı konumunu belirsiz bırakmaktadır."],
    ["Rosenborg'un Norveç'teki iddialı konumu, Avrupa kupalarında oynamayı ve Avrupa scout ekranlarına girmeyi kolaylaştırır.",
     "Norveç Milli Takımı savunmasındaki nesil değişimi, onu ulusal kadroya dahil olma yolunda önemli bir aday konumuna getiriyor.",
     "İyi bir form serisinin ardından İskandinav dışında orta bütçeli Avrupa kulüplerinin transfer hedefi olmaya aday olabilir."],
    ["Uzun süre resmi maç oynamamanın getirdiği gelişim boşluğu, yaşı için kritik olan patlama dönemini kaçırma riskini barındırır.",
     "Rosenborg'un rekabetçi savunma hattındaki konumlanma, forma alma sürecini uzatabilir ve motivasyonu olumsuz etkileyebilir.",
     "Maç eksiğinin ardından aniden üst düzey tempoyla karşılaşmak, kas sakatlıkları ve performans düşüklüğü riskini artırmaktadır."]
),

"Karoline Haugland": sw(
    ["Defansif ve merkez orta saha (DM, M C) pozisyonlarında görev alabilmesi, Brann'ın top kazanma ve oyun inşası süreçlerine çift boyutlu katkı sunmaktadır.",
     "Brann'ın Norveç ligindeki ve Şampiyonlar Ligi'ndeki prestijli konumu, oyuncuya üst düzey rekabet ortamında yeteneklerini sergileme imkânı sağlıyor.",
     "77/100 FM26 puanı, saha ortasındaki kontrolcü ve yıkıcı rolde üst düzey bir potansiyele ve gelişim eğrisine sahip olduğuna işaret eder."],
    ["Bu sezon hiç resmi maç oynamamış olması, maç içi refleks, kondisyon ve takım kimyası açısından ciddi bir geri kalmışlık yaratmaktadır.",
     "Hücuma katkı istatistiklerinin sıfırda olması, oyun kurma ve yaratıcılık rolleri yerine tamamen top kesme odaklı bir profil sergilendiğine işaret edebilir.",
     "Fiziksel ölçülerin bilinmemesi, özellikle hava topları ve uzun koşular gerektiren orta saha müdahalelerindeki etkinliği hakkında belirsizlik yaratır."],
    ["Brann'ın Avrupa platformu, İskandinav dışı liglerdeki scout ekranlarında görünürlüğü artıracak stratejik bir fırsat sunmaktadır.",
     "Norveç Milli Takımı orta saha rotasyonuna dahil olma potansiyeli, uluslararası kariyer yolculuğunu hızlandırabilir.",
     "İyi bir form serisinin ardından, Almanya ve Danimarka gibi orta bütçeli liglerin transfer talip listelerine girme kapısı açılabilir."],
    ["Maçsız dönemin uzaması, fiziksel kondisyon kaybının ötesinde taktiksel otomatizm ve oryantasyon sorunlarına da yol açabilir.",
     "Brann'ın orta saha rekabetinin yüksekliği, oyuncunun motivasyonunu ve ilerleme hızını uzun vadede olumsuz etkileyebilir.",
     "İskandinav ligleri dışına yapılacak olası bir erken transferde yeni ligdeki oyun hızına uyum süreci beklentilerin altında kalabilir."]
),

"Stine Brekken": sw(
    ["DM ve merkez orta saha (DM, M C) kombinasyonundaki yetkinlik, Vålerenga'nın oyun kontrol ve savunmaya geçiş süreçlerinde kilit rol oynamasını sağlar.",
     "Vålerenga gibi Norveç'in güçlü kulüplerinden birinde forma giymesi, taktik disiplin ve rekabet ortamı açısından kaliteli bir eğitim almış olduğunu gösteriyor.",
     "77/100 FM26 notu, defansif duran topları bozmada ve pressing döngülerinde üst düzey performans sergilediğini kanıtlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, maç içi otomatizm ve yüksek yoğunluklu tempo performansı açısından önemli bir eksiklik oluşturmaktadır.",
     "İstatistiklerin tamamının sıfırda olması, pas kalitesi ve oyun kurma becerisinin nesnel olarak değerlendirilmesini güçleştiriyor.",
     "Fiziksel verilerinin bilinmemesi, daha fiziksel liglerdeki uzun koşu ve mücadele etkinliği konusunda belirsizlik taşımaktadır."],
    ["Vålerenga'nın hem ulusal hem de olası Avrupa katılımı, görünürlüğünü İskandinav sınırlarının ötesine taşıma potansiyeli barındırıyor.",
     "Norveç Milli Takımı'nın orta saha kadrosu için güçlü bir aday olan oyuncu, turnuva dönemlerinde uluslararası kariyer basamağını tırmanabilir.",
     "İkili orta saha rolündeki yetkinliği, farklı taktik sistemlerde oynatılabilecek esnek bir transfer profili oluşturmaktadır."],
    ["Uzun süreli maç eksikliği, orta saha oyuncularında kritik olan reaksiyon süresini ve top algısını köreltebilir.",
     "Vålerenga'nın rekabetçi orta saha kadrosu, oyuncunun forma alma mücadelesini uzatarak kariyer planlarını sekteye uğratabilir.",
     "DM profilindeki oyuncuların sahada kendini kanıtlaması için gereken yoğun istatistiksel katkının sıfırda kalması, transfer değerini olumsuz etkiler."]
),

"Eline Hegg": sw(
    ["Sağ kanat bek, sağ/merkez orta saha ve sağ/sol/merkez hücum sahası (WB R, M RC, AM RLC) genelinde istisnai bir çok yönlülük sergileyen nadir bir profil ortaya koyuyor.",
     "Vålerenga'da yüksek rekabetli Norveç liginde bu geniş yelpazedeki esnekliği geliştirmiş olması, taktiksel adaptasyon kapasitesini kanıtlıyor.",
     "77/100 FM26 puanı, söz konusu çok yönlülüğün yüzeysel değil derinlikli bir teknik kapasite ve oyun IQ'suyla desteklendiğini göstermektedir."],
    ["Bu sezon resmi maçta süre alamamış olması, aktif mücadeleden uzak kaldığını ve form düzeyinin belirlenemediğini işaret etmektedir.",
     "Çok sayıda pozisyonda yer alabilmesi, en güçlü olduğu birincil role odaklanmayı engelleyerek derinlemesine gelişimi sekteye uğratabilir.",
     "Gol ve asist verilerinin sıfırda olması, özellikle ofansif rollerdeki son pas kalitesi ve bitiricilik konusunda soru işareti bırakmaktadır."],
    ["Koridordan çok yönlü tehdit oluşturan bu profil, değişken sistemler kullanan Avrupa kulüplerinin scouting listelerinde üst sıralarda yer alabilir.",
     "Norveç Milli Takımı'nın taktik esnek kadrosunda kendine yer bularak uluslararası arenada görünürlüğünü artırabilir.",
     "Sahaya döndüğünde göstereceği yüksek uyum kapasitesi, Bundesliga ya da WSL gibi hızlı liglerde dahi kendine yer bulmasını kolaylaştırır."],
    ["Pozisyon bolluğu, teknik direktörlerin gözünde net bir rol belirleyememesine ve kadro planlamasında belirsizlik yaratmasına neden olabilir.",
     "Uzun süreli maçsız dönem, bu kadar geniş pozisyon yelpazesini sürdüren bir oyuncunun kas ve koordinasyon düzeyinde belirgin gerilemeye yol açabilir.",
     "Adaptasyon yeteneğine aşırı bağımlı kalınması, özgün bir teknik kimlik geliştirmeyi zorlaştırabilir ve transfer değerini sınırlayabilir."]
),

"Jelena Karličić": sw(
    ["Hem sağ bek hem de sağ kanat açık oyuncu (D RL, AM R) pozisyonlarında görev alabilmesi, savunma-hücum geçişlerinde takıma yüksek taktiksel esneklik kazandırır.",
     "Beşiktaş'ta 87 resmi maç oynamış olması, Türk Kadın Futbol Süper Ligi'nin zorlu rekabet ortamında edinilmiş zengin bir deneyime sahip olduğunu kanıtlar.",
     "10 gol atma başarısı ve 170 cm boyuyla hem ofansif hem defansif katkı sağlayan çok boyutlu bir Karadağlı oyuncu profili sergilenmektedir."],
    ["Mevcut sezon istatistiklerinin sıfır olması, son dönemde form kaybı ya da ciddi bir sakatlık sürecinde olabileceğine işaret etmektedir.",
     "Asist verisinin bulunmaması, yaratıcı son pas ve oyun kurma katkısının zayıf kaldığını göstermektedir.",
     "Piyasa değerinin 40.000 € seviyesinde olması, transfer piyasasındaki algının potansiyelinin altında kaldığını ve ticari değer eksikliğini yansıtmaktadır."],
    ["Türk liginde biriktirdiği uzun soluklu deneyim ve gol üretimi, Avrupa liglerine geçiş için güçlü bir baz oluşturuyor.",
     "Karadağ Milli Takımı formasıyla uluslararası düzeyde görünürlük kazanarak küresel transfer piyasasında farkındalık yaratabilir.",
     "İkili pozisyon bilgisi, farklı sistemlerde oynayan kulüpler için düşük maliyetli ama yüksek verimli bir transfer fırsatı sunar."],
    ["Kariyer süresince tek bir ligde kalmak, taktik repertuvar çeşitliliğini ve uyum esnekliğini sınırlayarak farklı liglere geçişi zorlaştırabilir.",
     "Milli takım kanalıyla uluslararası rekabete maruz kalma fırsatlarının kısıtlı olması, küresel ölçekte keşfedilme sürecini uzatmaktadır.",
     "Mevcut sezon istatistiklerinin düşük olması, 76/100 FM26 potansiyelinin transfer taleplerini karşılayacak düzeyde gerçeğe dönüşmediğini gösteriyor."]
),

"Aurora Mikalsen": sw(
    ["1. FC Köln gibi Almanya Bundesliga'nın köklü kulüplerinden birinde bulunması, Alman kaleci ekolünün teknik eğitimine ve yüksek rekabetine maruz kaldığını göstermektedir.",
     "76/100 FM26 puanı, Norveçli bu genç kalecinin refleks kapasitesi ve ceza sahası yönetimi açısından ciddi bir potansiyel taşıdığını tescilliyor.",
     "Norveç kökenli bir kaleci olarak, top oyunuyla düzlem ve yüksek pasörlük becerilerini beraberinde getiren teknik bir profil sergilemektedir."],
    ["Bu sezon hiç resmi maça çıkmamış olması, maç ritmi ve yüksek baskı altında oynama refleksi açısından ciddi bir açık oluşturmaktadır.",
     "Bundesliga standartlarındaki yoğun kaleci rekabeti, oyuncunun formayı kapma ve ilk 11'de yer alma sürecini uzatmaktadır.",
     "Fiziksel verilerinin belirsizliği, özellikle uzun çıkışlar ve yüksek toplar üzerindeki dominant konumunu değerlendirmeyi güçleştirmektedir."],
    ["Bundesliga'da elde edeceği ilk süre şansını değerlendirerek, üst ligdeki diğer takımların transfer planlarına girebilir.",
     "Norveç Milli Takımı'nın gelecek jenerasyonuna dahil olarak uluslararası arenada olgunluk kazanma fırsatı bulabilir.",
     "Köln'de kaleci antrenörünün sağlayacağı bireysel geliştirme programı, 76'lık potansiyelini daha hızlı gerçeğe dönüştürmesini sağlayabilir."],
    ["Bundesliga'nın yoğun kaleci derinliği karşısında bekleme sürecinin uzaması, gelişimini kritik bir dönemde duraksatabilir.",
     "Maç oynamadan geçirilen uzun dönem, özellikle kaleciler için yaşamsal olan refleks keskinliği ve ani tepki hızını köreltebilir.",
     "Köln'ün kadro planlaması, oyuncuyu uzun vadede yedek kaleci rolüne mahkûm edebilir ve potansiyelini sınırlayabilir."]
),

"Sunniva Skoglund": sw(
    ["76/100 FM26 notu, Stabæk'te Norveç ligi standardında kalecilik pratiği yapan genç bir kaleciyle ilgili umut verici bir profil çiziyor.",
     "İskandinav kaleci ekolünden gelmesi, top oyunu ve ayakla oyun kurma açısından teknik altyapının güçlü olduğuna işaret eder.",
     "Stabæk'in Norveç ligindeki uzun soluklu deneyimi, oyuncuya kültürel ve taktiksel anlamda tutarlı bir gelişim ortamı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut hazırlık ve rekabete uyum düzeyi hakkında ciddi belirsizlik yaratmaktadır.",
     "Fiziksel verilerin bilinmemesi, özellikle uzun oyun kurma çıkışlarında ve pozisyon almadaki fiziksel avantaj–dezavantaj analizini güçleştirmektedir.",
     "Gol ve asist istatistiklerinin sıfırda olması, kaleciler için ölçüt olmayan bu verilerden öte maç etkinliğinin değerlendirilmesini olanaksız kılmaktadır."],
    ["Norveç liginin küresel görünürlüğünü artıran yayın anlaşmaları, genç yeteneklerin Avrupa'nın daha geniş piyasalarında fark edilmesini hızlandırmaktadır.",
     "Stabæk'te mevcut kalecilerin form kaybetmesi ya da sakatlık yaşaması durumunda ilk 11'e çıkma ve kendini kanıtlama fırsatı doğabilir.",
     "Norveç Milli Takımı'nın genç kaleci rotasyonuna dahil olarak uluslararası karşılaşmalar aracılığıyla değer kazanabilir."],
    ["Uzun süreli resmi maçtan uzak kalma, kaleci pozisyonunda kritik önem taşıyan zamanlama ve ani refleks tepkilerinin körelmesine yol açabilir.",
     "Norveç ligindeki genç kaleci derinliği, oyuncunun forma alma şansını kısıtlayabilir ve motivasyon üzerinde olumsuz baskı oluşturabilir.",
     "İskandinav ligleri dışındaki yüksek tempolu Avrupa liglerinden erken bir transfer fırsatı geldiğinde, maç deneyimi eksikliği adaptasyonu zorlaştırabilir."]
),

"Sofia Reidy": sw(
    ["Hem sağ hem de sol ve merkez bek (D RLC) olarak oynayabilmesi, savunma hattında teknik direktöre son derece geniş bir yerleşim esnekliği sağlar.",
     "Hammarby IF'in Damallsvenskan'daki rekabetçi yapısı, oyuncuya İsveç liginin üst düzey taktiksel eğitim ortamını sunmaktadır.",
     "75/100 FM26 notu, üç bek pozisyonundaki yetkinliğinin yüzeysel değil derinlemesine bir teknik altyapıyla desteklendiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, maç kondisyonu ve anlık karar verme hızı açısından önemli bir geri kalmışlık yaratmaktadır.",
     "Üç bek pozisyonundaki esneklik, belirli bir anda en güçlü olduğu rol için net bir marka değeri oluşturulmasını zorlaştırabilir.",
     "Gol ve asist katkısının sıfırda olması, özellikle bek pozisyonlarında beklenen hücuma katkının henüz somutlaşmadığını göstermektedir."],
    ["İsveç liginin Avrupa kulüpleriyle sık transfer ilişkisi, oyuncunun erken yaşta daha büyük liglere adım atmasını kolaylaştırır.",
     "İsveç Milli Takımı'nın tutarlı uluslararası başarısı, ulusal kadrolara alınarak büyük platformlarda görünürlük kazanma şansı sunar.",
     "Üç pozisyondaki esnekliği, kadro derinliği ve yaralanma yönetimi odaklı transfer arayan kulüpler için özellikle değerli bir profil oluşturur."],
    ["İsveç liginin üst liglerle fiziksel ve taktiksel farkı, daha hızlı ve güçlü liglere geçişte adaptasyon güçlüklerine neden olabilir.",
     "Pozisyon çok yönlülüğünün yarattığı rol belirsizliği, teknik direktörlerin onu kalıcı bir ilk 11 oyuncusu olarak planlamasını zorlaştırabilir.",
     "Uzun maçsız dönem, özellikle savunma hattında gerekli olan pozisyon ve kapama otomatizmini köreltme riski taşımaktadır."]
),

"Maïté Boucly": sw(
    ["Sol koridorda savunmadan hücuma kadar geniş bir yelpazede (D/WB/M/AM L, ST C) faaliyet gösterebilmesi, onu takımın sol aksında tam anlamıyla özgün kılan bir profil oluşturuyor.",
     "Havre FC'de D1 Féminine deneyimi kazanması, Fransa'nın en rekabetçi ligindeki taktiksel uyum kapasitesini ve çok yönlü gelişimini kanıtlar.",
     "75/100 FM26 notu, sol koridordaki bu geniş yelpazeli yetkinliğin gerçek bir teknik kapasite ve oyun zekasıyla desteklendiğini göstermektedir."],
    ["Bu sezon resmi maç oynamamış olması, aktif formdaki gerçek performansını değerlendirmeyi ve mevcut kondisyon düzeyini belirlemeyi olanaksız kılmaktadır.",
     "Sol koridordaki bu geniş yelpaze, hangi rolde en verimli olduğunun belirsizleşmesine ve teknik direktörün bilinç dışı tercih sorununa yol açabilir.",
     "Fiziksel ölçülerin bilinmemesi, özellikle sol kanat bek ya da sol açık oyuncu olarak bir-bir savunma mücadelelerindeki etkinliği sorgulatmaktadır."],
    ["D1 Féminine'in küresel yayın ağları ve scout faaliyetleri, oyuncunun üst liglerin radarına girmesini hızlandırabilir.",
     "Sol koridordaki bütüncül profili, özellikle kanat oyunu ağırlıklı taktik sistem kullanan Avrupa kulüpleri için nadiren bulunan bir transfer çözümü sunar.",
     "Fransa Milli Takımı'nın sol kanat kadrosu için güçlü bir uzun vadeli alternatif olarak değerlendirilebilir."],
    ["Çok sayıda pozisyonda yer alabilmesi, rakipler tarafından taktiksel olarak hazırlık yapılmasını kolaylaştırmakta ve sürpriz etkisini azaltmaktadır.",
     "D1 Féminine'de uzun süreli maç eksiği, ligdeki hızlı forma gelişen rakipler karşısında konumunu zayıflatabilir.",
     "Sol ayaklı oyuncuların birçok pozisyonda aynı anda talep görmesi, bu alandaki rekabeti artırmakta ve daha güçlü rakiplerle kıyaslanmasına neden olmaktadır."]
),

"Maja Sternad": sw(
    ["Sol kanat ve sol-sağ ofansif orta saha (M L, AM RL) olarak ikili boyutta hücum katkısı sunabilmesi, SV Werder Bremen'e sol aksında önemli taktiksel seçenekler kazandırıyor.",
     "Slovenya'nın uluslararası arenada yükselen futbol kültürü ve Bundesliga ortamı, oyuncunun teknik gelişimini destekleyen disiplinli bir altyapı sunmaktadır.",
     "75/100 FM26 notu, sol kanattaki hücum yaratıcılığı ve dinamik koşu kapasitesi açısından oldukça umut verici bir potansiyele sahip olduğunu gösteriyor."],
    ["Bu sezon hiç resmi maça çıkmamış olması, maç içi ritim ve anlık karar hızı konusundaki hazırlık durumunun bilinmemesine yol açmaktadır.",
     "İstatistiksel verilerin tamamının sıfırda olması, özellikle yaratıcı pas kalitesi ve son bölgedeki üretkenliği analiz etmeyi imkânsız kılmaktadır.",
     "Sol kanatta hız ve teknik ağırlıklı bir profil için fiziksel ölçülerin bilinmemesi, üst düzey beklere karşı savunma mücadelelerindeki başarı oranını belirsizleştiriyor."],
    ["Bundesliga'nın teknik altyapısı ve Werder Bremen'in genç yetenekleri geliştirme geçmişi, oyuncunun potansiyelini hızla gerçeğe dönüştürmesi için ideal bir zemin sunuyor.",
     "Slovenya Milli Takımı'nda hücum kapasitesini sergileyen oyuncu, uluslararası turnuvalarda görünürlük kazanarak değerini artırabilir.",
     "Bundesliga platformu, sol kanadın yaratıcılığına önem veren WSL ve Ligue 1 gibi liglerin transfer ilgisini çekebilir."],
    ["Almanya'nın sol kanat oyuncularının yoğun rekabeti, forma alma sürecini uzatarak gelişim boşluklarına zemin hazırlayabilir.",
     "Maçsız uzun dönem, özellikle hız ve sürpriz unsuru üzerine kurulu kanat profillerinde ciddi performans gerileme riskini beraberinde getirir.",
     "Bundesliga'daki üst düzey fiziksel tempo ve sertliğe uyum sağlamakta zorlanmak, ligden ayrılma ya da küçülme kararına zemin hazırlayabilir."]
),

"Monica": sw(
    ["Sağ orta ve sağ ofansif orta saha (M/AM R) pozisyonundaki yetkinlik, AC Milan'ın sağ aksında hem kontrol hem yaratıcılık sağlayan değerli bir katkı sunuyor.",
     "Serie A Femminile'nin en prestijli kulüplerinden biri olan Milan bünyesinde bulunması, İtalya futbolunun üst düzey taktiksel ekolüne entegre olduğunun kanıtıdır.",
     "75/100 FM26 puanı, son bölgedeki teknik kalite ve oyun açma becerisiyle dikkat çeken bir İtalyan orta saha profili ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, aktif form ve maç kondisyonu açısından değerlendirme yapılmasını güçleştirmektedir.",
     "Gol ve asist istatistiklerinin sıfırda olması, hücum üretkenliği ve son pas kalitesiyle ilgili nesnel veriye ulaşmayı imkânsız kılmaktadır.",
     "Fiziksel bilgilerin eksikliği, yoğun mücadele gerektiren sağ kanat çizgisindeki bireysel duello performansını belirsizleştirmektedir."],
    ["Milan altyapısı ve Serie A platformu, oyuncunun uluslararası kulüp turnuvalarında görünürlük kazanması için paha biçilmez bir fırsat sunuyor.",
     "İtalya Milli Takımı'nın sağ kanat orta sahada arayışı devam ettiği sürece ulusal kadroya dahil olma şansı canlı kalmaktadır.",
     "Milan bünyesindeki dünya standartlarındaki antrenör kadrosu ve tesisler, kariyer ivmesini hızlandıracak bireysel gelişim planlarına olanak sağlıyor."],
    ["Milan'ın derin ve rekabetçi kadrosu, forma mücadelesinde daha deneyimli oyuncuların gerisinde kalmayı sürekli hale getirebilir.",
     "Serie A'nın yoğun ve fiziksel yapısına uyum sağlamakta zorlanan oyuncular için uzun süreli maçsız dönem, kalıcı form düşüklüğüne dönüşebilir.",
     "Uzun süre resmi maçta yer almamak, Milano'nun yoğun scout gözlemlerine rağmen transfer piyasasında gerçek piyasa değerinin belirsiz kalmasına neden olur."]
),

"Poppy Lawson": sw(
    ["İngiltere altyapısından gelen Hibernian'lı bu merkez defansçı, 74/100 FM26 notu ve stoper pozisyonundaki sağlam savunma kurgusunu temsil etmektedir.",
     "İskoçya SWPL'deki rekabetçi ortam, oyuncuya çeşitli hücum tiplerine karşı savunma deneyimi kazandırmakta ve adaptasyon kapasitesini güçlendirmektedir.",
     "İngilizce konuşan bir kültürden gelmesi, WSL ve FAWSL gibi üst liglere geçiş sürecinde dil ve kültürel adaptasyon engelini ortadan kaldırır."],
    ["Bu sezon resmi maç süresinin bulunmaması, mevcut kondisyon ve oyuna hazırlık durumuna ilişkin ciddi belirsizlik yaratmaktadır.",
     "İskoçya liginin ortalama rekabet düzeyinin İngiltere ve Almanya'ya kıyasla görece düşük olması, üst liglere geçişte sürpriz adaptasyon sorunları yaşanmasına neden olabilir.",
     "Gol ve asist istatistiklerinin sıfırda olması, duran toplarda hücum katkısı ve geriden pas açma kalitesi konusunda değerlendirme yapmayı güçleştirmektedir."],
    ["İngiltere Milli Takımı ya da alt milli takımları için seçilmek, uluslararası görünürlük açısından kariyerini hızlı biçimde ilerletebilir.",
     "WSL kulüplerinin İskoçya'daki genç yeteneklere ilgisi, Hibernian platformundan değer kazanarak üst liga transfer yapma kapısını açmaktadır.",
     "Stoper pozisyonunda İngiliz pasaportuna sahip olması, kota odaklı WSL transferlerinde ekstra bir avantaj sağlamaktadır."],
    ["İskoçya'dan WSL'e geçişte yaşanacak taktiksel ve fiziksel uyum zorluğu, ilk sezonda beklentilerin altında kalma riskini beraberinde getirir.",
     "Maçsız uzun dönem, stoper pozisyonunda hayati önem taşıyan anlık karar verme ve savunma koordinasyonu açısından gerileme riski taşımaktadır.",
     "Bilinmeyen bir profil olarak WSL'in yoğun transfer piyasasında dikkat çekememek, geç bir kariyer ilerleme sürecine yol açabilir."]
),

"Julia Magerl": sw(
    ["Merkez defans (D C) rolünde RB Leipzig'in Bundesliga standardındaki disiplinli savunma yapısı içinde çalışması, taktiksel gelişim açısından değerli bir ortam sağlamaktadır.",
     "74/100 FM26 puanı ve Avusturya kökenli bir stoper olarak, güçlü pressing anlayışı ve bireysel duel kapasitesiyle öne çıkmaktadır.",
     "Leipzig'in genç oyuncuları geliştirmeye yönelik sistematik altyapısı, oyuncunun potansiyelini gerçeğe dönüştürme sürecini desteklemektedir."],
    ["Bu sezon resmi maçta hiç süre alamamış olması, mevcut hazırlık ve maç ritmi konusundaki değerlendirmeyi olanaksız kılmaktadır.",
     "Bundesliga'nın agresif hücum temposuna karşı savunma tepkisinin pratikte test edilmemiş olması, üst düzey rekabete hazırlık konusunda soru işaretleri doğurmaktadır.",
     "Fiziksel parametrelerin bilinmemesi, özellikle hava topları ve fiziksel güç gerektiren mücadelelerdeki etkinliği hakkında değerlendirme yapmayı zorlaştırıyor."],
    ["RB Leipzig'in Almanya'daki güçlü marka değeri ve scout ağı, oyuncunun Avrupa çapında tanınmasını hızlandırabilir.",
     "Avusturya Milli Takımı'nın savunma kadrosundaki genç yenilenme süreci, onu ulusal düzeyde önemli bir aday konumuna getirebilir.",
     "Bundesliga platformundan yapılacak kiralık bir transferle maç deneyimi kazanarak, 74'lük potansiyelini somutlaştırma fırsatı ortaya çıkabilir."],
    ["Bundesliga'nın yoğun ve fiziksel rekabet ortamına uyum sağlamakta zorlanmak, uzun vadeli kadro planlamasının dışına düşme riskini barındırır.",
     "Leipzig savunma hattındaki mevcut oyuncuların performansının yüksek olması, forma alma şansını uzun vadede kısıtlayabilir.",
     "Avusturya'nın küresel futbol arenasındaki görece sınırlı temsil gücü, scout ilgisinin gecikmesine ve transfer fırsatlarının daralmasına yol açabilir."]
),

"Selma Pettersen": sw(
    ["Sol ve merkez bek (D LC) pozisyonlarındaki ikili yetkinlik, Vålerenga'nın savunma hattında hem sağdan hem de soldan operasyonel esneklik kazandırıyor.",
     "Vålerenga'da üst düzey Norveç liginde forma mücadelesine giren oyuncu, rekabetçi bir ortamın sağladığı taktiksel olgunluğu geliştirmektedir.",
     "74/100 FM26 puanı, sol-merkez defans kombinasyonundaki kapasitesinin teknik analistler tarafından üst sıralarda değerlendirildiğini ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, aktif rekabet ortamından kopukluk ve kondisyon belirsizliği yaratmaktadır.",
     "Gol ve asist katkısının sıfırda olması, özellikle sol bek profilinde beklenen hücuma destek ve son bölge katkısını sorgulatmaktadır.",
     "Fiziksel verilerin bilinmemesi, hava topu mücadelelerindeki dominant konumu ve fiziksel kapasitesi konusunda belirsizlik bırakmaktadır."],
    ["Vålerenga'nın olası Avrupa kupası katılımları, oyuncunun küresel ölçekte tanınması için değerli bir vitrin oluşturabilir.",
     "Norveç Milli Takımı'nın genç sol bek havuzuna dahil olması, uluslararası kariyer ivmesini hızlandırabilecek kritik bir adımdır.",
     "İkili bek pozisyonundaki esnekliği, farklı savunma sistemleri kullanan transfer talep eden kulüpler için cazip bir profil oluşturmaktadır."],
    ["Vålerenga'daki savunma rekabetinin yüksekliği, oyuncunun forma almasını kısıtlayabilir ve uzun vadeli gelişimini sekteye uğratabilir.",
     "Norveç liginin Avrupa'daki görece sınırlı bilinirliği, yabancı kulüplerin ilgisinin gecikmesine zemin hazırlayabilir.",
     "Maçsız uzun dönemin ardından forma dönüşlerde kondisyon açığını kapatma sürecindeki olası sakatlıklar, gelişim ivmesini kırabileceği kritik bir risk unsuru oluşturur."]
),

"Julia Pollak": sw(
    ["Sol bek ve sol kanat bek (D/WB L) pozisyonlarındaki esneklik, 1. FC Nürnberg'in sol koridorunda hem savunma güvenliği hem hücum derinliği sağlıyor.",
     "Alman futbol kültüründen gelmesi ve 2. Bundesliga'da rekabet etmesi, yüksek taktiksel disiplin ve pressing verimliliği açısından güçlü bir temel sunmaktadır.",
     "74/100 FM26 puanı, bu profil için kritik olan hız, sol ayak kalitesi ve savunmadan hücuma geçiş becerisinde yüksek notlara ulaştığını gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form düzeyi ve maç kondisyonu konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücuma katkı istatistiklerinin sıfırda olması, kanat bek profilinde beklenen son bölge katkısının henüz somutlaşmadığını ortaya koymaktadır.",
     "Fiziksel verilerin belirsizliği, özellikle sol koridorda bir-bir mücadele ve çapraz top kalitesi konusunda analiz yapmayı zorlaştırıyor."],
    ["2. Bundesliga'nın Almanya'nın scout ağıyla yakın ilişkisi, onu Bundesliga'nın dikkat ekranlarına erken dönemde taşıyabilir.",
     "Almanya Milli Takımı altyapılarında bu profil için açık bir ihtiyaç olması, ulusal kariyer basamağını tırmanma fırsatı sunmaktadır.",
     "Sol kanat bek pozisyonuna artan talep, farklı taktik sistemlerdeki kulüpler için onu rekabetçi bir transfer hedefi konumuna getirir."],
    ["2. Bundesliga'dan Bundesliga'ya geçişteki fiziksel ve taktiksel tempo farkı, adaptasyon döneminde performans düşüklüğüne zemin hazırlayabilir.",
     "Nürnberg'in mevcut sol kanat rekabetinin yüksek olması, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir.",
     "Uzun süreli maçsız dönem, sol kanat oyuncularında kritik önem taşıyan hız patlayıcılığı ve top sürme kapasitesi üzerinde olumsuz etki yaratabilir."]
),

"Maja Hagermann": sw(
    ["Hem defansif hem de sol/merkez orta saha (DM, M LC) olarak oynaması, Sassuolo'nun orta sahasında hem koruyucu hem de organizasyon rolünü üstlenme kapasitesi sağlıyor.",
     "Danimarkalı bir oyuncu olarak Serie A Femminile'nin zorlu rekabet ortamında yer alması, yüksek seviyeli taktiksel ve fiziksel adaptasyon kapasitesine sahip olduğunu kanıtlar.",
     "74/100 FM26 puanı, hem savunma bloğunu oluşturma hem de oyun kurma süreçlerindeki teknik kaliteyle üst düzey bir orta saha profili ortaya koyuyor."],
    ["Bu sezon resmi maçta süre alamamış olması, maç ritmi, taktiksel entegrasyon ve yüksek baskıya tepki açısından belirsizlik oluşturmaktadır.",
     "Hücuma katkı istatistiklerinin sıfırda olması, DM-M kombinasyonundaki oyuncu için bile son pas ve skor üretimi katkısını sorgulatmaktadır.",
     "Fiziksel verilerin belirsizliği, özellikle hava topu ve uzun koşulardaki enerji yönetimi konusundaki performansı hakkında değerlendirme yapmayı güçleştirir."],
    ["Serie A Femminile'nin İtalyan futboluna katkı sağlayan uluslararası profil zenginliği, Danimarkalı oyuncunun global transfer ağlarına girişini kolaylaştırıyor.",
     "Danimarka Milli Takımı'nın orta saha ihtiyacı, oyuncuya uluslararası arenada kariyer ivmesini artırma şansı sunmaktadır.",
     "İtalyan futbol anlayışındaki taktiksel derinlik sayesinde, Sassuolo'dan ayrılırken çok daha olgun ve çok yönlü bir orta saha profili sergileyebilir."],
    ["Uzun süreli maçsız dönem, İtalya'nın fiziksel ve taktiksel açıdan zorlu ortamına uyum sürecini daha da uzatarak gelişim açısından kritik bir dönemin kaçırılmasına neden olabilir.",
     "Sassuolo'nun İtalyan oyuncularını ön plana çıkarma eğilimi, yabancı uyruklu bir oyuncu için sistematik bir rekabet dezavantajı oluşturabilir.",
     "DM pozisyonundaki yoğun rekabet, oyuncunun formayı alabilmesi için fark yaratacak bireysel performans göstermesini daha kritik hale getirmektedir."]
),

"Duda Serrana": sw(
    ["Ofansif orta saha (AM C) pozisyonundaki yaratıcı profil, São Paulo gibi Güney Amerika'nın teknik futbol anlayışını benimseyen kulübün hücum organizasyonunda belirleyici bir rol üstleniyor.",
     "Brezilya futbol ekolünün getirdiği dar alan tekniği, ritim değişimi ve top driblingi, ofansif orta saha için olmazsa olmaz bireysel katkı repertuvarını kapsamaktadır.",
     "73/100 FM26 puanı, global çapta yetenekli ofansif oyuncularla dolu Brezilya piyasasında bile üst sıralarda değerlendirilen umut vadeden bir profili temsil ediyor."],
    ["Bu sezon resmi maçta hiç süre alamamış olması, mevcut kondisyon ve Brezilyalı tempoya uyum konusundaki gerçek durumu belirsizleştirmektedir.",
     "Hücuma katkı istatistiklerinin sıfırda olması, birincil rolü gereği beklenen gol ve asist üretimindeki etkinliği hakkında değerlendirme yapılmasını imkânsız kılmaktadır.",
     "Fiziksel verilerinin bilinmemesi, özellikle orta saha rekabetinde fiziksel baskı altında oyun okuma ve top saklama becerisini belirsiz bırakmaktadır."],
    ["Brezilya'nın artan uluslararası futbol görünürlüğü ve FIFA platformu, oyuncunun Avrupa kulüplerinin scouting ağlarına erken dönemde dahil olmasını kolaylaştırmaktadır.",
     "Brezilya Milli Takımı'nın dünya genelindeki mediatik etkisi ve yayın ağları, oyuncunun kariyer profilini küresel ölçekte güçlendirme fırsatı sunuyor.",
     "AM C pozisyonundaki teknik profil, NWSL ve Ligue 1 gibi yaratıcı oyunculara değer veren liglerin transfer talebine uygun bir piyasa değeri oluşturabilir."],
    ["Brezilya'daki yüksek rekabet düzeyi ve çok sayıda ofansif yeteneğin varlığı, oyuncunun transfer piyasasında öne çıkmasını zorlaştırabilir.",
     "Avrupalı kulüpler için yetersiz görülebilecek Güney Amerika izleme ağlarının sınırları, Scout faaliyetlerinin geciktirilmesine neden olabilir.",
     "Maçsız dönemden kaynaklanan ofansif ritim kaybı, birincil rolüne dönüşte skor üretiminde beklentilerin altında kalmaya neden olabilir."]
),

"Emma Reshane": sw(
    ["Sol ve sağ bek, sol kanat bek, sol ve sağ orta/açık hücumcu (D RL, WB L, M/AM RL) genelinde oldukça geniş bir çok yönlülük, teknik direktöre sol ve sağ koridorlarda kapsamlı taktiksel esneklik sunuyor.",
     "LSK gibi Norveç'in rekabetçi kulüplerinden birinde bu geniş yelpazeli profili geliştirmesi, futbol IQ'sunun ve çabuk adaptasyon kapasitesinin güçlü olduğunu kanıtlar.",
     "71/100 FM26 puanı, söz konusu çok yönlülüğün yüzeysel değil derinlemesine bir teknik kapasite ve anlık karar verme becerisiyle desteklendiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut form düzeyi ve rekabete hazırlık konusundaki belirsizliği artırmaktadır.",
     "Bu denli geniş bir pozisyon yelpazesi, hangi rolde en verimli katkıyı sunabileceğinin belirsizleşmesine yol açarak teknik direktörün planlamasını güçleştirebilir.",
     "Gol ve asist istatistiklerinin sıfırda olması, kanat odaklı bu pozisyonlarda beklenen hücum katkısını değerlendirmeyi olanaksız kılmaktadır."],
    ["Çift kanat esnekliği, farklı sistemler kullanan kulüpler için kolayca uyum sağlayabilen nadir bir transfer profili oluşturur.",
     "Norveç Milli Takımı'nda tam anlamıyla çok yönlü bir joker oyuncu rolüne soyunarak uluslararası kariyer basamağını tırmanabilir.",
     "LSK'da sağlanacak düzenli maç süresi, bu zengin pozisyon repertuvarını somutlaştırma ve transfer piyasasında değer yaratma adına kritik bir fırsat sunacaktır."],
    ["Çok sayıda pozisyonda yer alabilmek, belirli bir uzmanlık alanı eksikliğine dönüşerek üst ligde spesifik rol arayışındaki kulüpler tarafından göz ardı edilmesine neden olabilir.",
     "Uzun süreli maçsız dönem, kanat oyuncularında kritik önem taşıyan hız patlayıcılığı ve topsuz koşu kapasitesinde kalıcı gerilemeye yol açabilir.",
     "Norveç liginin uluslararası görünürlüğünün sınırlı olması, bu geniş yetenekli profilin çok daha büyük platformlar tarafından keşfedilmesini geciktirebilir."]
),

"Lucie Calba": sw(
    ["Sol ve merkez açık hücumcu ile santrafor (AM LC, ST C) pozisyonlarındaki ikili yetkinlik, FC Nantes'ın hücumunda hem kanat hem ön bölge tehdidi yaratma kapasitesi sunuyor.",
     "D1 Féminine'nin rekabetçi yapısında forma mücadelesi veren oyuncu, Fransız kadın futbolunun yüksek taktiksel standartlarında gelişme fırsatı bulmuştur.",
     "71/100 FM26 puanı, sol kanat yaratıcılığı ve hücum bitiriciliğini harmanlayan dinamik bir profil için makul düzeyde değerlendirildiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut kondisyon ve hücum ritmindeki hazırlık durumunu belirsizleştirmektedir.",
     "Hücum odaklı pozisyonlarda beklenen gol ve asist istatistiklerinin sıfırda olması, skor üretim kapasitesi konusunda soru işaretleri doğurmaktadır.",
     "Fiziksel verilerin bilinmemesi, özellikle son bölgedeki topbaşı mücadelelerinde ve hız koşularındaki etkinliği belirsiz bırakmaktadır."],
    ["D1 Féminine'nin küresel yayın platformları ve scout trafiği, oyuncunun uluslararası transfer piyasasına erken dönemde adım atmasını kolaylaştırır.",
     "Sol kanat ve santrafor kombinasyonundaki profil, farklı hücum sistemleri kullanan Avrupa kulüpleri için cazip bir katkı sunmaktadır.",
     "Fransa Milli Takımı altyapılarında bu profil için açık bir ihtiyaç, ulusal kariyer basamağını tırmanma fırsatını güçlendirmektedir."],
    ["D1 Féminine'in rekabetçi hücum oyuncu profili, sıra dışı bir form serisi olmadan öne çıkmayı zorlaştırmaktadır.",
     "Maçsız uzun dönem, özellikle hız ve son bölge refleksleri açısından kritik olan bireysel formun geride kalmasına neden olabilir.",
     "Sol kanat ve santrafor rolleri arasındaki ikili konumlanma, spesifik bir rol arayan kulüplerde açık bir kimlik boşluğu oluşturabilir."]
),

"Laura Pucks": sw(
    ["Merkez defans (D C) pozisyonunda SGS Essen'in Bundesliga standardındaki savunma kurgusunda görev alması, taktiksel disiplin ve kapama verimliliği açısından güçlü bir altyapı sağlamaktadır.",
     "71/100 FM26 notu, Alman savunma ekolünün getirdiği top kazanma etkinliği ve bireysel duel başarısında üst sıralarda değerlendirildiğini gösteriyor.",
     "SGS Essen'in savunmaya yönelik sistematik oyun modeli, oyuncunun savunma organizasyonu ve pozisyon alma bilgisini güçlü biçimde geliştirmektedir."],
    ["Bu sezon resmi maçta süre alamamış olması, maç kondisyonu ve rekabete aktif uyum konusundaki hazırlık durumunu belirsizleştirmektedir.",
     "Gol ve asist istatistiklerinin sıfırda olması, duran toplardaki ofansif katkı ve geriden oyun açma konusundaki yetkinliği değerlendirmeyi güçleştirmektedir.",
     "Fiziksel verilerinin belirsizliği, özellikle santrforlara karşı bir-bir savunmadaki güç ve hız dengesini analiz etmeyi olanaksız kılmaktadır."],
    ["Bundesliga'nın Almanya scout ağıyla güçlü bağlantısı, oyuncunun daha büyük kulüplerin transfer listesine girmesini hızlandırabilir.",
     "Almanya Milli Takımı'nın genç savunma havuzu için güçlü bir aday olan oyuncu, seçilmesi durumunda kariyer ivmesini hızla yükseltebilir.",
     "SGS Essen'in savunma akademisi, kişisel antrenman programları ve bireysel gelişim planlarıyla oyuncunun 71'lik potansiyelini aşmasına katkı sağlayabilir."],
    ["Bundesliga'nın yoğun tempo ve fiziksel rekabeti, uzun maçsız dönem sonrasında forma dönerken ciddi adaptasyon güçlüklerine zemin hazırlayabilir.",
     "Essen'deki mevcut stoper rekabeti, forma şansını uzun vadede kısıtlayarak gelişim hızını yavaşlatabilir.",
     "Almanya'nın derin savunma kadrosu, üst ligdeki bek pozisyonları için çok sayıda rakibin varlığı göz önüne alındığında transfer ilgisini geciktirebilir."]
),

"Léa Notel": sw(
    ["Sol ve merkez bek (D LC) pozisyonlarındaki çift yönlü yetkinlik, bonservis gerektirmeksizin hemen transfer edilebilir olması nedeniyle kadro derinliği arayan kulüpler için maliyet avantajı sağlamaktadır.",
     "Fransa futbol ekolünden gelen serbest oyuncu, D1 Féminine standartlarında savunma tecrübesine sahip olup piyasada uygun maliyetli bir çözüm sunmaktadır.",
     "71/100 FM26 notu, serbest oyuncu olmasına karşın teknik kapasitesinin üst sıralarda değerlendirildiğini, yatırım değeri açısından güçlü bir profil oluşturduğunu gösteriyor."],
    ["Serbest oyuncu statüsü, herhangi bir takım sistemine entegre olmamış olmasından kaynaklanan kondisyon eksikliği ve ritim kaybı riskini beraberinde getirir.",
     "Bu sezon resmi maçta süre alamamış olması, aktif formunu ve sahaya hazırlık düzeyini değerlendirmeyi güçleştirmektedir.",
     "Fiziksel verilerinin bilinmemesi, özellikle sol bek pozisyonundaki hız, güç ve hava topu etkinliği konusunda belirsizlik yaratmaktadır."],
    ["Bonservis bedelsiz transfer edilebilmesi, bütçe kısıtlaması olan küçük ve orta bütçeli kulüpler için anlık bir savunma çözümü sunmaktadır.",
     "Sol ve merkez bek kombinasyonu, kısa sürede birden fazla pozisyonda katkı yapabileceği takımlar için pratik bir tercih olabilir.",
     "Doğru teknik direktör eşleşmesi ve sistematik bir yeniden entegrasyon planı, 71'lik potansiyelini kaliteli bir sezonla sahaya yansıtma şansı sunmaktadır."],
    ["Uzun süre takım sisteminden uzak kalmak, sözleşme müzakerelerinde beklentilerin düşük tutulmasına ve özgüven kaybına yol açabilir.",
     "Bonservis bedelsiz transfer durumu, bazen oyuncunun piyasa değerinin düşüklüğüyle özdeşleştirilmesine ve caydırıcı bir algıya neden olabilir.",
     "Rekabetçi bir transferde şartları belirleyecek baskı gücünün olmaması, ideal olmayan bir kulüp ya da sisteme dahil olma riskini barındırır."]
),

"Maria Grazia Petrara": sw(
    ["Merkez orta saha (M C) pozisyonunda Ternana Women'ın Serie A Femminile standartlarındaki taktiksel ortamında yetişmesi, savunmadan hücuma oyun kurma becerisini desteklemektedir.",
     "71/100 FM26 puanı, İtalyan orta saha ekolünün önem verdiği dar alan geçişi, tempo kontrolü ve pozisyon disiplini konularında üst sıralarda değerlendirildiğini gösteriyor.",
     "İtalya'nın taktik odaklı liginde edinen deneyim, oyunu okuma ve zaman kazanma becerisiyle pasif bekleme değil aktif oyun inşası gerçekleştirme kapasitesine sahip olduğuna işaret ediyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form düzeyi ve rekabete uyum konusundaki hazırlığını belirsizleştirmektedir.",
     "İstatistiklerinin tamamının sıfırda olması, hücuma katkı, pas isabeti ve top kazanma oranları gibi nesnel parametrelerin analiz edilmesini güçleştirmektedir.",
     "Fiziksel verilerinin bilinmemesi, özellikle orta saha mücadelelerinde güç ve hız dengesi konusunda değerlendirme yapmayı olanaksız kılmaktadır."],
    ["Serie A Femminile'nin üst liglerle olan scout ilişkisi, oyuncunun kariyerini hızla ilerletmek için değerli bir vitrin sunmaktadır.",
     "İtalya Milli Takımı'nın orta sahada genç nesil arayışı, ulusal kariyer basamağını tırmanma açısından zamanlamanın uygun olduğuna işaret etmektedir.",
     "Serie A'nın taktik disiplininde şekillenen bir oyuncu olarak, farklı Avrupa liglerinin oyun anlayışlarına hızlıca adapte olabilme kapasitesine sahiptir."],
    ["Ternana Women'ın rekabetçi kadrosundaki yüksek mücadele ortamı, düzenli forma almasını zorlaştırabilir ve gelişim ivmesini yavaşlatabilir.",
     "Uzun süreli maçsız dönem, orta saha oyuncuları için hayati önem taşıyan ritim, zamanlama ve otomatik tepki reflekslerinde gerilemeye neden olabilir.",
     "İtalyan liginin kendi ülkesindeki oyunculara öncelik verme eğilimi, yabancı kulüplerin ilgisini çekmek için daha fazla saha saati ve kanıt gerektirmektedir."]
),

"Jenna Ferguson": sw(
    ["Merkez defans (D C) pozisyonunda İskoçya SWPL'in rekabetçi yapısında forma mücadelesi veren oyuncu, İskoç futbol ekolünün getirdiği sertlik ve mücadele azmiyle dikkat çekmektedir.",
     "70/100 FM26 puanı, Partick Thistle gibi geleneksel bir kulüpte savunma disiplini ve mücadele kapasitesi açısından makul bir kariyer potansiyeli sergilediğini gösteriyor.",
     "İskoçya pasaportu, WSL ve FAWSL gibi büyük İngiliz liglerine geçiş sürecinde kota gereksinimi olmaksızın kolayca transfer edilebilme avantajı sağlamaktadır."],
    ["Bu sezon resmi maçta süre alamamış olması, kondisyon ve rekabete aktif uyum konusundaki hazırlık durumunu belirsizleştirmektedir.",
     "SWPL'in fiziksel ve taktiksel düzeyi ile WSL arasındaki ciddi fark, üst liga transferinde adaptasyon güçlüklerine zemin hazırlayabilir.",
     "İstatistiklerinin tamamının sıfırda olması, geriden oyun kurma kalitesi ve hücuma katkı etkinliğini değerlendirmeyi güçleştirmektedir."],
    ["İskoçya Milli Takımı seçilebilirliği, uluslararası arenada farkındalık yaratarak kariyer görünürlüğünü hızla artırma fırsatı sunmaktadır.",
     "WSL kulüplerinin İskoçya'daki uygun maliyetli yeteneklere olan ilgisi, Partick Thistle platformundan transfer kapısını aralamaktadır.",
     "İskoçya pasaportunun sağladığı kota avantajı, rakip yabancı stopertler karşısında ciddi bir tercih önceliği oluşturmaktadır."],
    ["SWPL'den WSL'e geçişte yaşanacak taktiksel ve fiziksel tempo farkı, ilk sezonda beklentilerin altında kalma riskini beraberinde getirir.",
     "Partick Thistle'ın sınırlı scout erişimi ve medya görünürlüğü, yeteneğinin geniş kitleler tarafından fark edilmesini geciktirebilir.",
     "Uzun süreli maçsız dönem, stoper pozisyonunda hayati önem taşıyan savunma koordinasyonu ve anlık karar verme konusunda gerileme riski taşımaktadır."]
),

"Macey Fraser": sw(
    ["Hem merkez hem de ofansif orta saha (M/AM C) pozisyonlarındaki ikili yetkinlik, Wellington Phoenix'in orta sahasında hem kontrol hem yaratıcılık sağlayan değerli bir profil sunuyor.",
     "Yeni Zelanda futbolunun artan uluslararası görünürlüğü, özellikle 2023 FIFA Dünya Kupası sonrasında, oyuncunun global transfer radarlarına girmesini hızlandırmaktadır.",
     "70/100 FM26 puanı, Okyanusya bölgesinin rekabetçi ortamında merkez hücum organizasyonu ve top kontrolü açısından üst sıralarda değerlendirildiğini gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, form düzeyi ve üst liglerle rekabete hazırlık konusundaki belirsizliği artırmaktadır.",
     "Yeni Zelanda ve Avustralya liglerinin Avrupa büyük liglerinden ciddi ölçüde ayrışan tempo ve taktik düzeyi, üst liga transferinde adaptasyon güçlükleri yaratabilir.",
     "Gol ve asist istatistiklerinin sıfırda olması, hücum katkısının ve son bölge üretkenliğinin değerlendirilmesini güçleştirmektedir."],
    ["Yeni Zelanda Milli Takımı formasıyla büyük turnuvalarda oynama, kariyer görünürlüğünü küresel ölçekte artırmanın en pratik yoludur.",
     "Avustralya A-League Women veya Asya'nın rekabetçi liglerinden birine geçiş, Avrupa transferi öncesinde taktiksel olgunluk kazanmayı sağlayabilir.",
     "Ofansif profili, NWSL gibi teknik ve hızlı liglerle de uyumlu olup kariyer seçeneklerini genişletmektedir."],
    ["Okyanusya'nın sınırlı global futbol temsili, Avrupalı scout ekranlarına çıkma sürecini önemli ölçüde geciktirebilir.",
     "Uzun süreli maçsız dönem, özellikle merkez–ofansif ikili rolde kritik olan tempo ve top duyarlılığı konusundaki form kaybına yol açabilir.",
     "Wellington Phoenix'in düşük uluslararası profili, kariyer planlaması açısından transfer fırsatlarını kısıtlayan bir çevre faktörü oluşturmaktadır."]
),

"Silje Helgesen": sw(
    ["Merkez defans (D C) pozisyonunda Stabæk'teki rekabetçi Norveç ligi deneyimi, savunma organizasyonu ve bireysel kapama becerileri açısından sağlam bir altyapı sağlamaktadır.",
     "70/100 FM26 puanı, Norveç savunma ekolünün getirdiği ikili mücadele kapasitesi ve pozisyon okuma becerisiyle desteklenen makul bir potansiyeli ortaya koyuyor.",
     "İskandinav kadın futbolunun küresel tanınırlığının artmasıyla birlikte, Norveç ligindeki her kaliteli stoper adayı artık daha geniş bir transfer ağına ulaşabilmektedir."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut kondisyon ve rekabete uyum düzeyi konusundaki değerlendirmeyi olanaksız kılmaktadır.",
     "İstatistiklerinin tamamının sıfırda olması, geriden oyun açma kalitesi ve hücuma sağladığı duran top katkısını analiz etmeyi güçleştirmektedir.",
     "Fiziksel verilerinin belirsizliği, hava topu mücadelelerindeki hakimiyeti ve fiziksel üstünlük ya da dezavantaj konusunda belirsizlik yaratmaktadır."],
    ["Stabæk'ten potansiyel bir kiralama transferi, maç eksiğini gidererek 70'lik scout puanını sahada somutlaştırma imkânı sunabilir.",
     "Norveç liginin Avrupa'daki artan bilinirliği ve scout trafiği, oyuncunun orta bütçeli Avrupa kulüplerinin radarına girme sürecini kısaltmaktadır.",
     "Norveç Milli Takımı'nın savunma nesil değişimi sürecinde, genç ve uygun maliyetli stoper alternatifi olarak değerlendirilebilir."],
    ["Stabæk'teki mevcut savunma rekabeti, oyuncunun forma almasını zorlaştırabilir ve kariyer ivmesini yavaşlatabilir.",
     "Uzun süreli maçsız dönem, stoper pozisyonunda hayati önem taşıyan savunma koordinasyonu ve anlık karar verme becerilerinin körelme riskini artırır.",
     "Norveç liginin Batı Avrupa büyük liglerinden fiziksel ve taktiksel olarak ayrışması, üst liga transferinde beklenmedik uyum güçlükleri yaratabilir."]
),

"Tuana Mahmoud": sw(
    ["Sol orta ve sol ofansif orta saha (M/AM L) pozisyonundaki yetkinlik ile Türk-Alman profili, SV Werder Bremen'in sol aksında yaratıcı ve dinamik bir tehdit unsuru oluşturuyor.",
     "Almanya Bundesliga ortamında forma mücadelesi veren oyuncu, yüksek taktiksel disiplin, fiziksel rekabet ve pressing anlayışı açısından üst düzey bir eğitim almaktadır.",
     "70/100 FM26 puanı, sol kanattaki sürü hızı ve top taşıma kapasitesiyle Almanya'nın rekabetçi sol kanat oyuncu havuzunda üst sıralarda yer bulduğunu gösteriyor."],
    ["Bu sezon resmi maçta süre alamamış olması, mevcut form ve maç ritmi konusundaki değerlendirmeyi güçleştirmektedir.",
     "Hücum istatistiklerinin tamamının sıfırda olması, son bölge üretkenliği ve asistin yanı sıra bireysel gol atma konusundaki etkinliği analiz etmeyi imkânsız kılmaktadır.",
     "Fiziksel verilerin belirsizliği, özellikle sol koridorda bir-bir mücadelede gereken hız ve güç dengesi konusunda net bir değerlendirme yapılmasını engellemektedir."],
    ["Almanya–Türkiye çift pasaportu, her iki ülkenin milli takım altyapılarına dahil olma şansı sunarak kariyer seçeneklerini genişletiyor.",
     "Bundesliga platformu, Alman sol kanat profilleri için talep gösteren İngiltere ve İspanya gibi liglerin transfer ilgisini çekebilir.",
     "Werder Bremen'in genç yeteneklere fırsat veren geliştirme politikası, düzenli maç süresi yakalamasını ve hızlı değer artışı sağlamasını kolaylaştırabilir."],
    ["Almanya'nın derin sol kanat oyuncu kadrosu, forma alma sürecini uzatarak gelişim ivmesini yavaşlatabilir.",
     "Bundesliga temposuna yeterli hazırlık olmaksızın sahaya çıkmak, hata yapma riskini artırabilir ve özgüven kaybına zemin hazırlayabilir.",
     "Maçsız uzun dönem, sol kanattaki kritik anlık esneme ve patlayıcı koşu kapasitesinin zaman içinde körelmesine yol açabilir."]
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

print(f"Part 1 done: {patched} SWOTs patched into data/hidden_gems.json")
