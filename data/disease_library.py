DISEASE_KNOWLEDGE_BASE = {
    potato: {
        Early Blight: {
            scientific_name: Alternaria solani,
            is_healthy: False,
            severity: Moderate,
            description: A common fungal disease causing concentric ring spots primarily on older foliage, reducing tuber yield.,
            causes: High humidity, warm temperatures (24-29°C), and alternating wet/dry periods.,
            symptoms: [
                Dark brown circular spots with characteristic concentric rings (target-board appearance),
                Yellowing chlorotic halo around leaf spots,
                Premature leaf drop starting from lower mature leaves,
                Dark sunken lesions on stems
            ],
            organic_remedies: [
                Apply cold-pressed Neem oil spray (5ml/L of water) every 7 to 10 days.,
                Prune lower canopy leaves up to 10-12 inches from soil to stop splashing.,
                Spray bio-fungicides containing Trichoderma viride or Bacillus subtilis.
            ],
            chemical_treatments: [
                Foliar spray of Copper Oxychloride 50 WP @ 2.5g per litre.,
                Mancozeb 75 WP (2.0g/L) or Chlorothalonil 75 WP (2.0g/L) at first symptom appearance.,
                Azoxystrobin 23 SC (1ml/L) for advanced protection.
            ],
            prevention: [
                Use certified disease-free potato seed tubers.,
                Apply 2-inch organic straw mulch to create a splash barrier.,
                Implement a 3-year crop rotation with non-solanaceous crops.,
                Use drip irrigation to prevent wetting leaf foliage.
            ]
        },
        Late Blight: {
            scientific_name: Phytophthora infestans,
            is_healthy: False,
            severity: Severe,
            description: A destructive oomycete water-mold disease that causes rapid foliage destruction and tuber rot within days.,
            causes: Cool temperatures (10-20°C) combined with high relative humidity (>90%) and frequent rainfall.,
            symptoms: [
                Irregular water-soaked brown/black necrotic lesions on leaves and stems,
                White fuzzy fungal growth on the underside of leaves during damp mornings,
                Petioles collapsing and emitting a distinctive pungent decay odor,
                Tubers developing dry brown corky rot beneath the skin
            ],
            organic_remedies: [
                Immediately remove and destroy (burn or bury) infected plants; never compost them.,
                Apply preventive copper hydroxide sprays before anticipated rainy spells.,
                Enhance hill soil coverage over tubers to prevent spore wash-down.
            ],
            chemical_treatments: [
                Emergency systemic spray: Metalaxyl 8% + Mancozeb 64% WP (2.5g/L).,
                Dimethomorph 50% WP (1.0g/L) combined with Mancozeb (2g/L).,
                Cymoxanil 8% + Mancozeb 64% WP (2g/L) applied during active outbreak.
            ],
            prevention: [
                Plant late blight-resistant potato cultivars.,
                Destroy cull piles and volunteer potato sprouts before the planting season.,
                Space plants properly (at least 60 cm row spacing) to promote rapid leaf drying.
            ]
        },
        Healthy: {
            scientific_name: N/A (Optimal Health),
            is_healthy: True,
            severity: None,
            description: Foliage is vibrant, robust, and free from pathogenic spots or wilting.,
            causes: Proper nutrition, optimal watering, and balanced sun exposure.,
            symptoms: [
                Vibrant emerald green compound leaves,
                Clean leaf margins without necrosis or chlorosis,
                Sturdy erect stems and healthy vegetative growth
            ],
            organic_remedies: [
                Maintain periodic compost and vermicompost soil enrichment.,
                Continue weekly visual scouting of lower leaves.
            ],
            chemical_treatments: [
                No chemical application needed.
            ],
            prevention: [
                Continue balanced N-P-K fertilization.,
                Maintain uniform moisture level via root-zone irrigation.
            ]
        }
    },
    tomato: {
        Early Blight: {
            scientific_name: Alternaria solani,
            is_healthy: False,
            severity: Moderate,
            description: Fungal pathogen that attacks foliage, stems, and fruit, creating target-pattern lesions.,
            causes: Warm humid conditions, soil splashing during rain, stressed plants.,
            symptoms: [
                Dark brown circular spots with concentric target-board rings on older foliage,
                Yellowing perimeter halo surrounding necrotic spots,
                Collar rot lesions at the soil line on young stems,
                Sunken leathery black spots near fruit calyx
            ],
            organic_remedies: [
                Spray cold-pressed Neem oil (5ml/L) at 7-day intervals.,
                Prune bottom 12 inches of suckers and foliage to improve airflow.,
                Apply compost tea foliar spray to boost beneficial microbial defense.
            ],
            chemical_treatments: [
                Copper Hydroxide or Copper Oxychloride 50 WP (2.5g/L).,
                Mancozeb 75 WP (2g/L) or Chlorothalonil 75 WP (2g/L).
            ],
            prevention: [
                Stake or cage tomato plants to keep leaves off the ground.,
                Mulch base with clean straw or black plastic mulch.,
                Water exclusively at soil level using drip emitters.
            ]
        },
        Late Blight: {
            scientific_name: Phytophthora infestans,
            is_healthy: False,
            severity: Severe,
            description: Highly aggressive pathogen causing complete vine collapse and fruit rot during cool, damp weather.,
            causes: Persistent moisture, cool nights (10-15°C) and mild days (15-22°C).,
            symptoms: [
                Large water-soaked dark brown to purplish lesions across leaves,
                Delicate white fungal down on leaf undersides in high humidity,
                Firm, greasy dark brown blotches on green or ripening tomatoes,
                Complete wilting and sudden blackening of foliage
            ],
            organic_remedies: [
                Rogue and safely bag/dispose of infected plants immediately.,
                Spray bio-fungicides with Bacillus subtilis.,
                Avoid working with plants when leaves are wet.
            ],
            chemical_treatments: [
                Metalaxyl + Mancozeb (2.5g/L) systemic spray.,
                Fenamidone 10% + Mancozeb 50% WG (2.5g/L).,
                Ametoctradin + Dimethomorph (1.5ml/L).
            ],
            prevention: [
                Plant certified resistant varieties (e.g., Defiant, Mountain Magic).,
                Avoid planting tomatoes adjacent to potato fields.,
                Provide wide spacing (75-90 cm) between plants for maximum air movement.
            ]
        },
        Septoria Leaf Spot: {
            scientific_name: Septoria lycopersici,
            is_healthy: False,
            severity: Moderate,
            description: Destructive fungal foliar disease producing numerous small circular lesions with dark borders and gray centers.,
            causes: Warm temperatures (20-25°C), high humidity, overhead watering.,
            symptoms: [
                Numerous small circular spots (2-3mm) with dark brown borders and pale grey centers,
                Tiny black specks (pycnidia) visible within spot centers under a lens,
                Progressive upward defoliation exposing fruit to sunscald
            ],
            organic_remedies: [
                Prune infected lower leaves as soon as first spots appear.,
                Apply potassium bicarbonate or liquid copper fungicides.,
                Sterilize pruning shears with 70% alcohol between cuts.
            ],
            chemical_treatments: [
                Chlorothalonil 75 WP (2g/L) or Mancozeb 75 WP (2g/L).,
                Pyraclostrobin or Azoxystrobin (1ml/L).
            ],
            prevention: [
                2-3 year crop rotation away from solanaceous species.,
                Deep tillage of crop residue at the end of the season.,
                Keep leaves dry by avoiding overhead sprinklers.
            ]
        },
        Healthy: {
            scientific_name: N/A (Optimal Health),
            is_healthy: True,
            severity: None,
            description: Vigorous tomato plant showing strong apical growth, green foliage, and healthy flowering.,
            causes: Optimal sun, balanced soil fertility, and controlled hydration.,
            symptoms: [
                Deep green lush foliage with healthy serrated leaf margins,
                Firm petioles and sturdy central vine growth,
                Normal flower bud formation without chlorosis
            ],
            organic_remedies: [
                Maintain regular organic feeding (liquid seaweed / fish fertilizer).,
                Apply regular mulch replenishment.
            ],
            chemical_treatments: [
                No chemical treatment needed.
            ],
            prevention: [
                Maintain 6-8 hours of direct daily sunlight.,
                Ensure balanced calcium and magnesium soil levels to prevent blossom end rot.
            ]
        }
    },
    apple: {
        Apple Scab: {
            scientific_name: Venturia inaequalis,
            is_healthy: False,
            severity: Severe,
            description: The most widespread fungal disease of apple orchards, causing olive-green to black velvety scabs on leaves and fruit.,
            causes: Overwintering in fallen leaves, prolonged springtime leaf wetness at 15-24°C.,
            symptoms: [
                Olive-green to velvety brown circular spots on upper leaf surfaces,
                Leaves becoming twisted, puckered, and dropping prematurely,
                Fruit developing dark corky, cracked, scabby lesions
            ],
            organic_remedies: [
                Rake and destroy fallen apple leaves in autumn to eliminate overwintering spores.,
                Apply sulfur-based or copper soap sprays during early bud break.,
                Prune tree canopy to maximize sun penetration and air circulation.
            ],
            chemical_treatments: [
                Captan 50 WP (2.5g/L) or Mancozeb 75 WP (2g/L) as protective sprays.,
                Myclobutanil 10 WP (1g/L) or Difenoconazole 25 EC (0.5ml/L) for curative action.
            ],
            prevention: [
                Plant scab-resistant apple cultivars (e.g., Enterprise, Liberty, Honeycrisp).,
                Apply urea spray (5%) to fallen orchard leaves in late autumn to accelerate decomposition.
            ]
        },
        Black Rot: {
            scientific_name: Botryosphaeria obtusa,
            is_healthy: False,
            severity: Severe,
            description: Fungal disease causing frog-eye leaf spots, limb cankers, and firm mummified black fruit rot.,
            causes: Dead wood, mummified apples, warm humid weather (24-27°C).,
            symptoms: [
                Frog-eye leaf spots: small purple specks expanding to circular spots with tan centers and purple borders,
                Sunken reddish-brown cankers on branches and limbs,
                Fruit developing brown rot with concentric black rings, turning into dry mummies
            ],
            organic_remedies: [
                Prune out dead wood, fire-blight strikes, and cankered branches 6 inches below infected zone.,
                Remove and dispose of all mummified fruit remaining on trees or orchard floor.,
                Lime sulfur sprays during dormant season.
            ],
            chemical_treatments: [
                Thiophanate-methyl 70 WP (1g/L) or Captan 50 WP (2g/L).,
                Flint (Trifloxystrobin) or Pristine (Pyraclostrobin + Boscalid).
            ],
            prevention: [
                Maintain tree vigor through balanced fertilization and insect control.,
                Disinfect pruning tools between cuts.
            ]
        },
        Cedar Apple Rust: {
            scientific_name: Gymnosporangium juniperi-virginianae,
            is_healthy: False,
            severity: Moderate,
            description: Heteroecious rust fungus requiring both apple trees and Eastern red cedar / juniper trees to complete its life cycle.,
            causes: Proximity to juniper/cedar trees, spring rains releasing spores from cedar galls.,
            symptoms: [
                Bright yellow-orange circular spots on upper apple leaf surfaces,
                Spots enlarging and developing reddish borders with tiny black dots,
                Underside of spots forming tube-like fringe structures (aecia),
                Early summer defoliation and dwarfed fruit
            ],
            organic_remedies: [
                Eradicate nearby wild juniper/cedar shrubs within a 500m radius if feasible.,
                Prune and remove galls from ornamental junipers during late winter.,
                Apply sulfur sprays beginning at pink bud stage.
            ],
            chemical_treatments: [
                Myclobutanil 10 WP (1g/L) or Mancozeb 75 WP (2g/L).,
                Propiconazole 25 EC (1ml/L) applied at tight cluster through petal fall.
            ],
            prevention: [
                Choose rust-resistant apple cultivars (e.g., Redfree, William's Pride).,
                Avoid planting apple orchards adjacent to cedar windbreaks.
            ]
        },
        Healthy: {
            scientific_name: N/A (Optimal Health),
            is_healthy: True,
            severity: None,
            description: Lush apple tree foliage with deep green color, strong shoot growth, and clean fruit spur development.,
            causes: Regular orchard hygiene, balanced nitrogen levels, and proactive canopy management.,
            symptoms: [
                Glossy, deep green leaves without rust spots, mildew, or scabs,
                Clean bark and active branch terminal extension,
                Healthy flower blossoms and fruit set
            ],
            organic_remedies: [
                Apply dormant oil spray in early spring for pest and scale control.,
                Maintain compost mulching around the drip line.
            ],
            chemical_treatments: [
                No fungicide required.
            ],
            prevention: [
                Perform annual winter pruning for optimal sun and airflow.,
                Maintain adequate boron and zinc micronutrient balance.
            ]
        }
    }
}
