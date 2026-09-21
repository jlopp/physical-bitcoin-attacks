#!/usr/bin/env python3
"""Enrich raw parsed attacks with lat/lng, city, country -> attacks.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "tools" / "raw_attacks.json"
OUT = ROOT / "attacks.json"

# location string (as in README) -> (city, region, country, iso2, lat, lng)
GEO = {
    # ---- United States ----
    "Atlanta, Georgia, United States": ("Atlanta", "Georgia", "United States", "US", 33.75, -84.39),
    "Bethesda, Maryland, United States": ("Bethesda", "Maryland", "United States", "US", 38.98, -77.10),
    "Brooklyn, New York, United States": ("Brooklyn", "New York", "United States", "US", 40.68, -73.94),
    "Chicago, Illinois, United States": ("Chicago", "Illinois", "United States", "US", 41.88, -87.63),
    "Cumming, Georgia, United States": ("Cumming", "Georgia", "United States", "US", 34.21, -84.14),
    "Danbury, Connecticut, United States": ("Danbury", "Connecticut", "United States", "US", 41.39, -73.45),
    "Delray Beach, Florida, United States": ("Delray Beach", "Florida", "United States", "US", 26.46, -80.07),
    "Durham, North Carolina, United States": ("Durham", "North Carolina", "United States", "US", 35.99, -78.90),
    "East Lansdowne, Pennsylvania, United States": ("East Lansdowne", "Pennsylvania", "United States", "US", 39.94, -75.27),
    "Grant, Minnesota, United States": ("Grant", "Minnesota", "United States", "US", 45.55, -93.86),
    "Homestead, Florida, United States": ("Homestead", "Florida", "United States", "US", 25.47, -80.48),
    "Houston, Texas, United States": ("Houston", "Texas", "United States", "US", 29.76, -95.37),
    "Irvine, California, United States": ("Irvine", "California", "United States", "US", 33.68, -117.79),
    "Irving & Mesquite, Texas, United States": ("Irving & Mesquite", "Texas", "United States", "US", 32.77, -96.80),
    "Irvinton, New York, United States": ("Irvington", "New York", "United States", "US", 41.04, -73.80),
    "Killingly, Connecticut, United States": ("Killingly", "Connecticut", "United States", "US", 41.84, -71.87),
    "Las Vegas, Nevada, United States": ("Las Vegas", "Nevada", "United States", "US", 36.17, -115.14),
    "Little Elm, Texas, United States": ("Little Elm", "Texas", "United States", "US", 33.16, -96.94),
    "Los Angeles, California, United States": ("Los Angeles", "California", "United States", "US", 34.05, -118.24),
    "Memphis, Tennessee, United States": ("Memphis", "Tennessee", "United States", "US", 35.15, -90.05),
    "Miami, Florida, United States": ("Miami", "Florida", "United States", "US", 25.76, -80.19),
    "Milwaukee, Wisconsin, United States": ("Milwaukee", "Wisconsin", "United States", "US", 43.04, -87.91),
    "Missouri, United States": ("Missouri", "", "United States", "US", 38.30, -92.50),
    "New York, New York, United States": ("New York", "New York", "United States", "US", 40.71, -74.01),
    "North Richmond Hills, Texas, United States": ("North Richland Hills", "Texas", "United States", "US", 32.83, -97.23),
    "Northborough, Massachussetts, United States": ("Northborough", "Massachusetts", "United States", "US", 42.35, -71.64),
    "Philadelphia, Pennsylvania, United States": ("Philadelphia", "Pennsylvania", "United States", "US", 39.95, -75.17),
    "Portland, Oregon, United States": ("Portland", "Oregon", "United States", "US", 45.52, -122.68),
    "Queens, New York, United States": ("Queens", "New York", "United States", "US", 40.73, -73.79),
    "San Francisco, California, United States": ("San Francisco", "California", "United States", "US", 37.77, -122.42),
    "San Jose, California, United States": ("San Jose", "California", "United States", "US", 37.34, -121.89),
    "Santa Barbara, California, United States": ("Santa Barbara", "California", "United States", "US", 34.42, -119.70),
    "South Bay, California, United States": ("South Bay (Silicon Valley)", "California", "United States", "US", 37.30, -121.90),
    "Scottsdale, Arizona, United States": ("Scottsdale", "Arizona", "United States", "US", 33.49, -111.93),
    "Seattle, Washington, United States": ("Seattle", "Washington", "United States", "US", 47.61, -122.33),
    "Sunnyvale, California, United States": ("Sunnyvale", "California", "United States", "US", 37.37, -122.04),
    "United States": ("United States", "", "United States", "US", 39.80, -98.60),
    "West Palm Beach, Florida, United States": ("West Palm Beach", "Florida", "United States", "US", 26.71, -80.05),
    "Winnetka, Illinois, United States": ("Winnetka", "Illinois", "United States", "US", 42.11, -87.74),
    "Winnsboro, Texas, United States": ("Winnsboro", "Texas", "United States", "US", 32.96, -95.29),
    # ---- United Kingdom ----
    "Blantyre, Scotland": ("Blantyre", "Scotland", "United Kingdom", "GB", 55.86, -4.09),
    "Bradford, Yorkshire, England": ("Bradford", "Yorkshire", "United Kingdom", "GB", 53.80, -1.75),
    "Cardishead, England": ("Cadishead", "", "United Kingdom", "GB", 53.43, -2.43),
    "Carlisle, England": ("Carlisle", "", "United Kingdom", "GB", 54.89, -2.93),
    "Far Cotton, Northampton, England": ("Northampton (Far Cotton)", "", "United Kingdom", "GB", 52.23, -0.90),
    "Kent, England": ("Kent", "", "United Kingdom", "GB", 51.20, 0.70),
    "Lincolnshire, England": ("Lincolnshire", "", "United Kingdom", "GB", 53.20, -0.20),
    "London, England": ("London", "", "United Kingdom", "GB", 51.51, -0.13),
    "Maidenhead, Berkshire, England": ("Maidenhead", "Berkshire", "United Kingdom", "GB", 51.52, -0.72),
    "Manchester, England": ("Manchester", "", "United Kingdom", "GB", 53.48, -2.24),
    "Moulsford, Oxfordshire, England": ("Moulsford", "Oxfordshire", "United Kingdom", "GB", 51.62, -1.14),
    "Oxford, England": ("Oxford", "", "United Kingdom", "GB", 51.75, -1.26),
    "Preston, Lancashire, England": ("Preston", "Lancashire", "United Kingdom", "GB", 53.76, -2.70),
    "Salford, England": ("Salford", "", "United Kingdom", "GB", 53.48, -2.29),
    "Sparkhill, Birmingham, England": ("Birmingham (Sparkhill)", "", "United Kingdom", "GB", 52.45, -1.88),
    # ---- France ----
    "Alès, Gard, France": ("Alès", "Gard", "France", "FR", 44.13, 4.08),
    "Angers, France": ("Angers", "", "France", "FR", 47.47, -0.55),
    "Anglet, France": ("Anglet", "", "France", "FR", 43.48, -1.51),
    "Bondy, Seine-Saint-Denis, France": ("Bondy", "Seine-Saint-Denis", "France", "FR", 48.90, 2.49),
    "Boulogne-Billancourt, France": ("Boulogne-Billancourt", "", "France", "FR", 48.83, 2.24),
    "Challes-les-Eaux, Savoie, France": ("Challes-les-Eaux", "Savoie", "France", "FR", 45.56, 5.99),
    "Chalon-sur-Saône, France": ("Chalon-sur-Saône", "", "France", "FR", 46.78, 4.85),
    "Cures, Sarthe, France": ("Cures", "Sarthe", "France", "FR", 47.96, 0.19),
    "Dijon, Côte-d’Or, France": ("Dijon", "Côte-d'Or", "France", "FR", 47.32, 5.04),
    "Essonne, France": ("Essonne", "", "France", "FR", 48.50, 2.40),
    "France": ("France", "", "France", "FR", 46.60, 2.30),
    "Gignac-la-Nerthe, France": ("Gignac-la-Nerthe", "", "France", "FR", 43.39, 5.22),
    "Jouy-en-Josas, France": ("Jouy-en-Josas", "", "France", "FR", 48.76, 2.27),
    "Juilly, Seine-et-Marne, France": ("Juilly", "Seine-et-Marne", "France", "FR", 48.98, 2.66),
    "Juvisy-sur-Orge, France": ("Juvisy-sur-Orge", "", "France", "FR", 48.76, 2.37),
    "La Chapelle-Saint-Aubin, Sarthe, France": ("La Chapelle-Saint-Aubin", "Sarthe", "France", "FR", 48.03, 0.17),
    "La Rochelle, France": ("La Rochelle", "", "France", "FR", 46.16, -1.15),
    "Le Chesnay-Rocquencourt, Yvelines, France": ("Le Chesnay-Rocquencourt", "Yvelines", "France", "FR", 48.83, 2.07),
    "Loire-Atlantique, France": ("Loire-Atlantique", "", "France", "FR", 47.30, -1.70),
    "Manosque, Alpes-de-Haute-Provence, France": ("Manosque", "Alpes-de-Haute-Provence", "France", "FR", 43.83, 5.78),
    "Marseille, France": ("Marseille", "", "France", "FR", 43.30, 5.37),
    "Montigny-le-Bretonneux, Yvelines, France": ("Montigny-le-Bretonneux", "Yvelines", "France", "FR", 48.78, 2.04),
    "Mulhouse, France": ("Mulhouse", "", "France", "FR", 47.75, 7.34),
    "Nancy, Meurthe-et-Moselle, France": ("Nancy", "Meurthe-et-Moselle", "France", "FR", 48.69, 6.18),
    "Nantes, France": ("Nantes", "", "France", "FR", 47.22, -1.55),
    "Nice, France": ("Nice", "", "France", "FR", 43.70, 7.27),
    "Normandie, France": ("Normandy", "", "France", "FR", 49.20, 0.40),
    "Ottrott , Bas-Rhin, France": ("Ottrott", "Bas-Rhin", "France", "FR", 48.46, 7.42),
    "Paris, France": ("Paris", "", "France", "FR", 48.86, 2.35),
    "Péchabou, Haute-Garonne, France": ("Péchabou", "Haute-Garonne", "France", "FR", 43.49, 1.50),
    "Plancher-Bas, France": ("Plancher-Bas", "", "France", "FR", 47.58, 6.83),
    "Ploudalmézeau, Finistère, France": ("Ploudalmézeau", "Finistère", "France", "FR", 48.61, -4.67),
    "Rambouillet, Yvelines, France": ("Rambouillet", "Yvelines", "France", "FR", 48.64, 1.83),
    "Revelles, Somme, France": ("Revelles", "Somme", "France", "FR", 49.86, 2.20),
    "Rion-des-Landes, France": ("Rion-des-Landes", "", "France", "FR", 43.88, -0.95),
    "Saint-Genis-Pouilly, France": ("Saint-Genis-Pouilly", "", "France", "FR", 46.25, 6.05),
    "Saint-Jean-de-Védas, France": ("Saint-Jean-de-Védas", "", "France", "FR", 43.57, 3.83),
    "Saint-Léger-sous-Cholet, Maine-et-Loire, France": ("Saint-Léger-sous-Cholet", "Maine-et-Loire", "France", "FR", 47.16, -0.74),
    "Saint-Martin-le-Vinoux, Isère, France": ("Saint-Martin-le-Vinoux", "Isère", "France", "FR", 45.21, 5.73),
    "Seine-et-Marne, France": ("Seine-et-Marne", "", "France", "FR", 48.60, 3.00),
    "Suresnes, France": ("Suresnes", "", "France", "FR", 48.86, 2.23),
    "Taninges, Haute-Savoie, France": ("Taninges", "Haute-Savoie", "France", "FR", 46.10, 6.58),
    "Toulon, Var, France": ("Toulon", "Var", "France", "FR", 43.12, 5.93),
    "Toulouse, France": ("Toulouse", "", "France", "FR", 43.60, 1.44),
    "Troyes, France": ("Troyes", "", "France", "FR", 48.30, 4.07),
    "Val-d'Oise, France": ("Val-d'Oise", "", "France", "FR", 49.10, 2.10),
    "Val-de-Marne, France": ("Val-de-Marne", "", "France", "FR", 48.78, 2.48),
    "Valence, Drôme, France": ("Valence", "Drôme", "France", "FR", 44.93, 4.89),
    "Vaucresson, Hauts-de-Seine, France": ("Vaucresson", "Hauts-de-Seine", "France", "FR", 48.84, 2.16),
    "Vendin-le-Vieil, France": ("Vendin-le-Vieil", "", "France", "FR", 50.44, 3.00),
    "Vaires-sur-Marne, Seine-et-Marne, France": ("Vaires-sur-Marne", "Seine-et-Marne", "France", "FR", 48.86, 2.61),
    "Verneuil-sur-Seine, Yvelines, France": ("Verneuil-sur-Seine", "Yvelines", "France", "FR", 48.97, 1.97),
    "Vern-sur-Seiche, Ille-et-Vilaine, France": ("Vern-sur-Seiche", "Ille-et-Vilaine", "France", "FR", 48.05, -1.65),
    "Vierzon, France": ("Vierzon", "", "France", "FR", 47.26, 2.08),
    "Strasbourg, Bas-Rhin, France": ("Strasbourg", "Bas-Rhin", "France", "FR", 48.58, 7.75),
    "Juvisy-sur-Orge, France": ("Juvisy-sur-Orge", "", "France", "FR", 48.76, 2.37),
    "Grivesnes, France": ("Grivesnes", "Somme", "France", "FR", 49.78, 2.47),
    "Maisons-Alfort, France": ("Maisons-Alfort", "", "France", "FR", 48.81, 2.44),
    "Recife, Brazil": ("Recife", "Pernambuco", "Brazil", "BR", -8.05, -34.90),
    "Sallanches, Haute-Savoie, France": ("Sallanches", "Haute-Savoie", "France", "FR", 45.94, 6.63),
    "Voiron, Isère, France": ("Voiron", "Isère", "France", "FR", 45.36, 5.59),
    # ---- Canada ----
    "Barrie, Ontario, Canada": ("Barrie", "Ontario", "Canada", "CA", 44.39, -79.69),
    "Calgary, Alberta, Canada": ("Calgary", "Alberta", "Canada", "CA", 51.05, -114.07),
    "Cambridge, Ontario, Canada": ("Cambridge", "Ontario", "Canada", "CA", 43.36, -80.31),
    "Kelowna, British Columbia, Canada": ("Kelowna", "British Columbia", "Canada", "CA", 49.89, -119.50),
    "Toronto, Ontario, Canada": ("Toronto", "Ontario", "Canada", "CA", 43.65, -79.38),
    "Montreal, Quebec, Canada": ("Montreal", "Quebec", "Canada", "CA", 45.50, -73.57),
    "Ottawa, Canada": ("Ottawa", "", "Canada", "CA", 45.42, -75.70),
    "Port Moody, British Columbia, Canada": ("Port Moody", "British Columbia", "Canada", "CA", 49.28, -122.85),
    "Richmond, British Columbia, Canada": ("Richmond", "British Columbia", "Canada", "CA", 49.17, -123.14),
    "Thunder Bay, Ontario, Canada": ("Thunder Bay", "Ontario", "Canada", "CA", 48.38, -89.25),
    "Verdun, Quebec, Canada": ("Verdun (Montreal)", "Quebec", "Canada", "CA", 45.43, -73.57),
    "Vernon, British Columbia, Canada": ("Vernon", "British Columbia", "Canada", "CA", 50.27, -119.27),
    "Victoriaville, Québec, Canada": ("Victoriaville", "Quebec", "Canada", "CA", 46.06, -71.96),
    "Winnipeg, Canada": ("Winnipeg", "Manitoba", "Canada", "CA", 49.90, -97.14),
    # ---- Netherlands ----
    "Amsterdam, Netherlands": ("Amsterdam", "", "Netherlands", "NL", 52.37, 4.90),
    "Delft, Netherlands": ("Delft", "", "Netherlands", "NL", 52.01, 4.36),
    "Drouwenerveen, Netherlands": ("Drouwenerveen", "Drenthe", "Netherlands", "NL", 52.98, 6.78),
    "Leeuwarden, Netherlands": ("Leeuwarden", "", "Netherlands", "NL", 53.20, 5.79),
    "Lelystad, Netherlands": ("Lelystad", "", "Netherlands", "NL", 52.51, 5.47),
    "Oudenbosch, Netherlands": ("Oudenbosch", "", "Netherlands", "NL", 51.59, 4.53),
    # ---- Hong Kong ----
    "Hong Kong": ("Hong Kong", "", "Hong Kong", "HK", 22.32, 114.17),
    "Chai Wan, Hong Kong": ("Chai Wan", "", "Hong Kong", "HK", 22.27, 114.24),
    "Hun Hom, Hong Kong": ("Hung Hom", "", "Hong Kong", "HK", 22.30, 114.19),
    "Kwun Tong, Hong Kong": ("Kwun Tong", "", "Hong Kong", "HK", 22.31, 114.22),
    "Lai Chi Kok, Hong Kong": ("Lai Chi Kok", "", "Hong Kong", "HK", 22.33, 114.15),
    "Mong Kok, Kowloon, Hong Kong": ("Mong Kok", "Kowloon", "Hong Kong", "HK", 22.32, 114.17),
    "North Point, Hong Kong": ("North Point", "", "Hong Kong", "HK", 22.29, 114.20),
    "Sheung Wan, Hong Kong": ("Sheung Wan", "", "Hong Kong", "HK", 22.29, 114.15),
    "Tseung Kwan, Hong Kong": ("Tseung Kwan O", "", "Hong Kong", "HK", 22.31, 114.26),
    "Tsim Sha Tsui, Hong Kong": ("Tsim Sha Tsui", "", "Hong Kong", "HK", 22.30, 114.17),
    # ---- Thailand ----
    "Bangkok, Thailand": ("Bangkok", "", "Thailand", "TH", 13.76, 100.50),
    "Phuket, Thailand": ("Phuket", "", "Thailand", "TH", 7.89, 98.39),
    "Koh Samui, Thailand": ("Koh Samui", "", "Thailand", "TH", 9.51, 100.01),
    "Samui Island, Thailand": ("Koh Samui", "", "Thailand", "TH", 9.51, 100.01),
    "Pattaya, Thailand": ("Pattaya", "", "Thailand", "TH", 12.93, 100.88),
    # ---- India ----
    "Ahmedabad, India": ("Ahmedabad", "Gujarat", "India", "IN", 23.03, 72.58),
    "Amreli, India": ("Amreli", "Gujarat", "India", "IN", 21.60, 71.22),
    "Bavdhan, India": ("Bavdhan (Pune)", "Maharashtra", "India", "IN", 18.51, 73.77),
    "Bengaluru, India": ("Bengaluru", "Karnataka", "India", "IN", 12.97, 77.59),
    "Dehradun, India": ("Dehradun", "Uttarakhand", "India", "IN", 30.32, 78.03),
    "Jaipur, Rajasthan, India": ("Jaipur", "Rajasthan", "India", "IN", 26.91, 75.79),
    "Jodhpur, India": ("Jodhpur", "Rajasthan", "India", "IN", 26.24, 73.02),
    "Noida, India": ("Noida", "Uttar Pradesh", "India", "IN", 28.54, 77.39),
    "Pune, India": ("Pune", "Maharashtra", "India", "IN", 18.52, 73.86),
    "Surat, India": ("Surat", "Gujarat", "India", "IN", 21.17, 72.83),
    "Vrindavan Yojana, India": ("Vrindavan Yojana (Lucknow)", "Uttar Pradesh", "India", "IN", 26.85, 81.00),
    # ---- Spain ----
    "Barcelona, Spain": ("Barcelona", "", "Spain", "ES", 41.39, 2.17),
    "Benalmádena, Spain": ("Benalmádena", "", "Spain", "ES", 36.60, -4.55),
    "Costa del Sol, Spain": ("Costa del Sol", "", "Spain", "ES", 36.50, -4.80),
    "Madrid, Spain": ("Madrid", "", "Spain", "ES", 40.42, -3.70),
    "Southern Spain": ("Southern Spain", "", "Spain", "ES", 36.80, -4.40),
    "Spain": ("Spain", "", "Spain", "ES", 40.20, -3.70),
    # ---- Brazil ----
    "Campo Limpo Paulista, Brazil": ("Campo Limpo Paulista", "São Paulo", "Brazil", "BR", 23.21, -46.70),
    "Florianopolis, Brazil": ("Florianópolis", "Santa Catarina", "Brazil", "BR", 27.60, -48.55),
    "Goiania, Brazil": ("Goiânia", "Goiás", "Brazil", "BR", 16.68, -49.25),
    "Imbiribeira, Brazil": ("Imbiribeira (Recife)", "Pernambuco", "Brazil", "BR", 8.09, -34.92),
    "Ipiranga, Brazil": ("Ipiranga (São Paulo)", "São Paulo", "Brazil", "BR", 23.63, -46.60),
    "Porto Velho, Rondônia, Brazil": ("Porto Velho", "Rondônia", "Brazil", "BR", 8.74, -63.90),
    "Ribeirão Preto, São Paulo, Brazil": ("Ribeirão Preto", "São Paulo", "Brazil", "BR", -21.18, -47.81),
    "Sao Paulo, Brazil": ("São Paulo", "", "Brazil", "BR", 23.55, -46.63),
    "São Paulo, Brazil": ("São Paulo", "", "Brazil", "BR", 23.55, -46.63),
    "Sao Pedro da Aldeia, Brazil": ("São Pedro da Aldeia", "Rio de Janeiro", "Brazil", "BR", 22.83, -42.10),
    "Vitória, Espírito Santo, Brazil": ("Vitória", "Espírito Santo", "Brazil", "BR", 20.32, -40.34),
    # ---- Ukraine ----
    "Kharkiv, Ukraine": ("Kharkiv", "", "Ukraine", "UA", 49.99, 36.23),
    "Kyiv, Ukraine": ("Kyiv", "", "Ukraine", "UA", 50.45, 30.52),
    "Odessa, Ukraine": ("Odessa", "", "Ukraine", "UA", 46.48, 30.73),
    "Ternopil, Ukraine": ("Ternopil", "", "Ukraine", "UA", 49.55, 25.59),
    "Zaporizhya, Ukraine": ("Zaporizhzhia", "", "Ukraine", "UA", 47.84, 35.14),
    # ---- Russia ----
    "Izhevsk, Russia": ("Izhevsk", "", "Russia", "RU", 56.85, 53.20),
    "Kuchino, Russia": ("Kuchino (Moscow Oblast)", "", "Russia", "RU", 55.75, 37.98),
    "Leningrad Oblast, Russia": ("Leningrad Oblast", "", "Russia", "RU", 60.00, 31.00),
    "Moscow, Russia": ("Moscow", "", "Russia", "RU", 55.76, 37.62),
    "Omsk, Russia": ("Omsk", "", "Russia", "RU", 54.99, 73.37),
    "St. Petersburg, Russia": ("St. Petersburg", "", "Russia", "RU", 59.93, 30.34),
    "Tomsk, Russia": ("Tomsk", "", "Russia", "RU", 56.49, 84.95),
    "Ufa, Russia": ("Ufa", "", "Russia", "RU", 54.74, 55.97),
    # ---- UAE ----
    "Dubai, UAE": ("Dubai", "", "United Arab Emirates", "AE", 25.20, 55.27),
    # ---- Singapore ----
    "Singapore": ("Singapore", "", "Singapore", "SG", 1.35, 103.82),
    "Hougang, Singapore": ("Hougang", "", "Singapore", "SG", 1.37, 103.89),
    "Lianhe Zaobao, Singapore": ("Singapore (Lianhe Zaobao)", "", "Singapore", "SG", 1.29, 103.85),
    # ---- Philippines ----
    "Philippines": ("Philippines", "", "Philippines", "PH", 12.90, 121.80),
    "Makati, Philippines": ("Makati", "Metro Manila", "Philippines", "PH", 14.56, 121.03),
    "Mecauayan, Bulacan, Philippines": ("Meycauayan", "Bulacan", "Philippines", "PH", 14.74, 120.96),
    "Parañaque City, Philippines": ("Parañaque", "Metro Manila", "Philippines", "PH", 14.48, 121.02),
    "Pasay City, Philippines": ("Pasay", "Metro Manila", "Philippines", "PH", 14.54, 121.00),
    # ---- Indonesia ----
    "Bali, Indonesia": ("Bali", "", "Indonesia", "ID", 8.41, 115.19),
    "Pecatu, Bali, Indonesia": ("Pecatu", "Bali", "Indonesia", "ID", 8.82, 115.17),
    "Sanur Beach, Bali, Indonesia": ("Sanur Beach", "Bali", "Indonesia", "ID", 8.70, 115.26),
    "Ungasan, Bali, Indonesia": ("Ungasan", "Bali", "Indonesia", "ID", 8.80, 115.16),
    # ---- Sweden ----
    "Norrköping, Sweden": ("Norrköping", "", "Sweden", "SE", 58.59, 16.19),
    "Rönninge, Sweden": ("Rönninge", "", "Sweden", "SE", 59.17, 17.76),
    "Sweden": ("Sweden", "", "Sweden", "SE", 60.10, 15.00),
    "Södertälje, Sweden": ("Södertälje", "", "Sweden", "SE", 59.20, 17.63),
    "Stockholm, Sweden": ("Stockholm", "", "Sweden", "SE", 59.33, 18.07),
    "Tierp, Sweden": ("Tierp", "", "Sweden", "SE", 60.34, 17.50),
    "Tobo, Sweden": ("Tobo", "Uppsala", "Sweden", "SE", 60.13, 17.92),
    # ---- Germany ----
    "Munich, Germany": ("Munich", "", "Germany", "DE", 48.14, 11.58),
    # ---- Belgium ----
    "Brussels, Belgium": ("Brussels", "", "Belgium", "BE", 50.85, 4.35),
    "Hoboken, Belgium": ("Hoboken (Antwerp)", "", "Belgium", "BE", 51.18, 4.36),
    "Zoersel, Belgium": ("Zoersel", "", "Belgium", "BE", 51.10, 4.69),
    # ---- Argentina ----
    "Buenos Aires, Argentina": ("Buenos Aires", "", "Argentina", "AR", -34.61, -58.38),
    "Mendoza, Argentina": ("Mendoza", "", "Argentina", "AR", -32.89, -68.84),
    "Villa Carlos Paz, Argentina": ("Villa Carlos Paz", "Córdoba", "Argentina", "AR", -31.42, -64.50),
    # ---- Australia ----
    "Melbourne, Australia": ("Melbourne", "Victoria", "Australia", "AU", 37.81, 144.96),
    "Sydney, Australia": ("Sydney", "New South Wales", "Australia", "AU", 33.87, 151.21),
    # ---- South Africa ----
    "Lanseria, South Africa": ("Lanseria (Johannesburg)", "", "South Africa", "ZA", 25.94, 27.93),
    # ---- Nigeria ----
    "Abraka, Nigeria": ("Abraka", "Delta", "Nigeria", "NG", 5.80, 6.08),
    "Lagos, Nigeria": ("Lagos", "", "Nigeria", "NG", 6.45, 3.39),
    "Okota, Lagos": ("Okota (Lagos)", "", "Nigeria", "NG", 6.47, 3.34),
    # ---- Pakistan ----
    "Karachi, Pakistan": ("Karachi", "Sindh", "Pakistan", "PK", 24.86, 67.01),
    "Gujranwala, Pakistan": ("Gujranwala", "Punjab", "Pakistan", "PK", 32.16, 74.19),
    "Kahna, Pakistan": ("Kahna (Lahore)", "Punjab", "Pakistan", "PK", 31.35, 74.35),
    "Lahore, Pakistan": ("Lahore", "Punjab", "Pakistan", "PK", 31.55, 74.34),
    "PIB Colony, Pakistan": ("PIB Colony (Karachi)", "Sindh", "Pakistan", "PK", 24.92, 67.06),
    # ---- Japan ----
    "Gifu, Japan": ("Gifu", "", "Japan", "JP", 35.39, 136.72),
    "Osaka, Japan": ("Osaka", "", "Japan", "JP", 34.69, 135.50),
    # ---- South Korea ----
    "Gyeonggi Province, South Korea": ("Gyeonggi Province", "", "South Korea", "KR", 37.40, 127.20),
    "Jeju, South Korea": ("Jeju", "", "South Korea", "KR", 33.50, 126.50),
    "Jeju City, South Korea": ("Jeju City", "", "South Korea", "KR", 33.50, 126.53),
    "Seoul, South Korea": ("Seoul", "", "South Korea", "KR", 37.57, 126.98),
    # ---- Israel ----
    "Herzliya, Israel": ("Herzliya", "", "Israel", "IL", 32.16, 34.84),
    "Tel Aviv, Israel": ("Tel Aviv", "", "Israel", "IL", 32.09, 34.78),
    # ---- Georgia / Abkhazia (map polygons: part of Georgia) ----
    "Abkhazia": ("Abkhazia", "", "Georgia", "GE", 43.00, 41.00),
    "Sukhumi, Abkhazia": ("Sukhumi", "Abkhazia", "Georgia", "GE", 43.00, 41.02),
    "Tbilisi, Georgia": ("Tbilisi", "", "Georgia", "GE", 41.72, 44.79),
    # ---- Poland ----
    "Olsztyn, Poland": ("Olsztyn", "", "Poland", "PL", 53.78, 20.48),
    # ---- Austria ----
    "Vienna, Austria": ("Vienna", "", "Austria", "AT", 48.21, 16.37),
    "Wels, Austria": ("Wels", "", "Austria", "AT", 48.17, 14.03),
    # ---- New Zealand ----
    "Westmere, New Zealand": ("Westmere (Auckland)", "", "New Zealand", "NZ", 36.87, 174.72),
    # ---- Iceland ----
    "Reykjavik, Iceland": ("Reykjavik", "", "Iceland", "IS", 64.15, -21.94),
    # ---- Norway ----
    "Oslo, Norway": ("Oslo", "", "Norway", "NO", 59.91, 10.75),
    # ---- Italy ----
    "Milan, Italy": ("Milan", "", "Italy", "IT", 45.46, 9.19),
    "Manerba, Italy": ("Manerba del Garda", "", "Italy", "IT", 45.58, 10.55),
    # ---- Baltic states ----
    "Kaunas, Lithuania": ("Kaunas", "", "Lithuania", "LT", 54.90, 23.93),
    "Riga, Latvia": ("Riga", "", "Latvia", "LV", 56.95, 24.11),
    "Talinn, Estonia": ("Tallinn", "", "Estonia", "EE", 59.44, 24.75),
    # ---- Others ----
    "Sliema, Malta": ("Sliema", "", "Malta", "MT", 35.91, 14.50),
    "Sofia, Bulgaria": ("Sofia", "", "Bulgaria", "BG", 42.70, 23.32),
    "Limassol, Cyprus": ("Limassol", "", "Cyprus", "CY", 34.68, 33.05),
    "Cluj, Romania": ("Cluj-Napoca", "", "Romania", "RO", 46.77, 23.60),
    "Colombo, Sri Lanka": ("Colombo", "", "Sri Lanka", "LK", 6.93, 79.86),
    "Ho Chi Minh City, Vietnam": ("Ho Chi Minh City", "", "Vietnam", "VN", 10.82, 106.63),
    "Chengdu, China": ("Chengdu", "Sichuan", "China", "CN", 30.57, 104.07),
    "China": ("China", "", "China", "CN", 35.00, 105.00),
    "Taichung, Taiwan": ("Taichung", "", "Taiwan", "TW", 24.15, 120.67),
    "Colombia": ("Colombia", "", "Colombia", "CO", 4.60, -74.10),
    "Medellin, Colombia": ("Medellín", "", "Colombia", "CO", 6.24, -75.58),
    "Montenegro": ("Montenegro", "", "Montenegro", "ME", 42.70, 19.40),
    "Istanbul, Turkey": ("Istanbul", "", "Turkey", "TR", 41.01, 28.98),
    "Arnavutköy, Istanbul, Turkey": ("Arnavutköy (Istanbul)", "", "Turkey", "TR", 41.18, 28.72),
    "Kampala, Uganda": ("Kampala", "", "Uganda", "UG", 0.35, 32.58),
    "Laboma Beach, Ghana": ("Laboma Beach (Accra)", "Greater Accra", "Ghana", "GH", 5.57, -0.18),
    "Puntarenas, Costa Rica": ("Puntarenas", "", "Costa Rica", "CR", 9.98, -84.84),
    "Atizapán de Zaragoza, Mexico": ("Atizapán de Zaragoza", "Estado de México", "Mexico", "MX", 19.56, -99.23),
    "Trincity, Trinidad and Tobago": ("Trincity", "", "Trinidad and Tobago", "TT", 10.63, -61.34),
    "Ciudad del Este, Alto Paraná, Paraguay": ("Ciudad del Este", "Alto Paraná", "Paraguay", "PY", 25.52, -54.64),
    "Coronel Bogado, Paraguay": ("Coronel Bogado", "Itapúa", "Paraguay", "PY", 27.44, -55.66),
    "Klang, Malaysia": ("Klang", "Selangor", "Malaysia", "MY", 3.04, 101.45),
    "Cyberjaya, Malaysia": ("Cyberjaya", "Selangor", "Malaysia", "MY", 2.92, 101.77),
    "Malacca, Malaysia": ("Malacca", "", "Malaysia", "MY", 2.20, 102.25),
}


def main():
    attacks = json.loads(RAW.read_text(encoding="utf-8"))
    missing = set()
    for a in attacks:
        g = GEO.get(a["location"])
        if g is None:
            missing.add(a["location"])
            continue
        city, region, country, iso2, lat, lng = g
        a["city"] = city
        a["region"] = region
        a["country"] = country
        a["country_code"] = iso2
        a["lat"] = lat
        a["lng"] = lng
    if missing:
        print("MISSING GEO:")
        for m in sorted(missing):
            print(f"  {m}")
        raise SystemExit(1)
    OUT.write_text(json.dumps(attacks, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {len(attacks)} attacks -> {OUT}")


if __name__ == "__main__":
    main()
