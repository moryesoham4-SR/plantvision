export const PLANTS = [
  {
    id: potato,
    name: Potato,
    scientificName: Solanum tuberosum,
    icon: 🥔,
    status: active,
    badge: Active Model,
    diseases: [Early Blight, Late Blight, Healthy]
  },
  {
    id: tomato,
    name: Tomato,
    scientificName: Solanum lycopersicum,
    icon: 🍅,
    status: active,
    badge: Active Model,
    diseases: [Early Blight, Late Blight, Septoria Leaf Spot, Healthy]
  },
  {
    id: apple,
    name: Apple,
    scientificName: Malus domestica,
    icon: 🍎,
    status: active,
    badge: Active Model,
    diseases: [Apple Scab, Black Rot, Cedar Apple Rust, Healthy]
  },
  {
    id: corn,
    name: Corn (Maize),
    scientificName: Zea mays,
    icon: 🌽,
    status: training,
    badge: Training 75%,
    diseases: [Leaf Blight, Common Rust, Healthy]
  },
  {
    id: grape,
    name: Grapevine,
    scientificName: Vitis vinifera,
    icon: 🍇,
    status: development,
    badge: Dataset Prep 40%,
    diseases: [Black Rot, Esca, Healthy]
  }
];

export const DISEASE_DATABASE = {
  potato: {
    Early Blight: {
      pathogen: Alternaria solani,
      isHealthy: false,
      severity: Moderate,
      description: Fungal disease causing concentric target-board brown rings on older lower leaves, lowering tuber yield.,
      causes: Warm humid temperatures (24-29°C), alternating dry and rainy spells, soil splash.,
      symptoms: [
        Dark brown circular spots with characteristic concentric rings (target pattern),
        Yellow chlorotic halo surrounding necrotic spots,
        Premature leaf drop beginning from lower canopy,
        Dark sunken lesions on mature stems
      ],
      remedies: {
        organic: [
          Spray cold-pressed Neem oil (5ml/L of water) every 7-10 days,
          Prune lower foliage up to 10-12 inches above soil line to stop splashing,
          Apply bio-fungicides with Trichoderma viride or Bacillus subtilis
        ],
        chemical: [
          Foliar spray of Copper Oxychloride 50 WP @ 2.5g per litre,
          Mancozeb 75 WP (2.0g/L) or Chlorothalonil 75 WP (2.0g/L),
          Azoxystrobin 23 SC (1ml/L) for curative protection
        ],
        prevention: [
          Plant certified disease-free seed tubers,
          Apply clean straw mulch as a rain splash barrier,
          Implement a 3-year crop rotation with non-solanaceous crops,
          Drip irrigation to keep foliage dry
        ]
      }
    },
    Late Blight: {
      pathogen: Phytophthora infestans,
      isHealthy: false,
      severity: Severe,
      description: Destructive oomycete water-mold disease that rapidly destroys foliage and rots tubers within days.,
      causes: Cool temperatures (10-20°C) with persistent high humidity (>90%) and rain.,
      symptoms: [
        Large irregular water-soaked dark brown/black lesions on leaves and stems,
        White delicate fuzzy fungal mycelium on leaf undersides in damp mornings,
        Petioles collapsing and emitting a distinctive rotting odor,
        Tubers developing dry brown corky rot beneath skin
      ],
      remedies: {
        organic: [
          Immediately remove and burn or deeply bury infected plants (never compost),
          Apply preventive copper hydroxide sprays before expected rain,
          Maintain thick soil hilling over tuber beds
        ],
        chemical: [
          Emergency systemic spray: Metalaxyl 8% + Mancozeb 64% WP (2.5g/L),
          Dimethomorph 50% WP (1.0g/L) + Mancozeb (2g/L),
          Cymoxanil 8% + Mancozeb 64% WP (2g/L)
        ],
        prevention: [
          Plant late blight-resistant potato cultivars,
          Destroy cull piles and volunteer potato sprouts before spring,
          Ensure wide row spacing (60 cm) for fast leaf drying
        ]
      }
    },
    Healthy: {
      pathogen: N/A (Optimal Foliage Health),
      isHealthy: true,
      severity: None,
      description: Plant foliage is vibrant, robust, and free from pathogenic spots, mildew, or wilting.,
      causes: Balanced N-P-K nutrition, optimal irrigation, and good sun exposure.,
      symptoms: [
        Vibrant emerald green compound leaves,
        Clean leaf margins without chlorosis or necrotic edges,
        Sturdy erect stems with vigorous vegetative growth
      ],
      remedies: {
        organic: [
          Maintain regular compost and vermicompost top-dressing,
          Continue weekly visual scouting of lower foliage
        ],
        chemical: [
          No chemical fungicide application needed
        ],
        prevention: [
          Maintain uniform moisture level via root-zone irrigation,
          Ensure 6-8 hours of direct daily sunlight
        ]
      }
    }
  },
  tomato: {
    Early Blight: {
      pathogen: Alternaria solani,
      isHealthy: false,
      severity: Moderate,
      description: Fungal pathogen attacking foliage, stems, and fruit, creating target-pattern lesions.,
      causes: Warm humid weather, soil splash during heavy rain, stressed vines.,
      symptoms: [
        Dark brown circular spots with concentric target rings on older foliage,
        Yellow chlorotic perimeter halo around spots,
        Collar rot lesions at soil line on young stems,
        Sunken leathery black lesions near fruit calyx
      ],
      remedies: {
        organic: [
          Spray cold-pressed Neem oil (5ml/L) at 7-day intervals,
          Prune bottom 12 inches of suckers and foliage to improve airflow,
          Compost tea foliar application to boost beneficial microflora
        ],
        chemical: [
          Copper Hydroxide or Copper Oxychloride 50 WP (2.5g/L),
          Mancozeb 75 WP (2g/L) or Chlorothalonil 75 WP (2g/L)
        ],
        prevention: [
          Stake or cage tomato vines to keep leaves elevated,
          Mulch base with straw or reflective plastic,
          Water strictly at ground level using drip emitters
        ]
      }
    },
    Late Blight: {
      pathogen: Phytophthora infestans,
      isHealthy: false,
      severity: Severe,
      description: Aggressive disease causing rapid vine collapse and fruit rot during cool, damp weather.,
      causes: Persistent moisture, cool nights (10-15°C) and mild days (15-22°C).,
      symptoms: [
        Large water-soaked dark brown to purplish lesions across leaves,
        Delicate white fungal down on leaf undersides during high humidity,
        Firm, greasy dark brown blotches on green or ripening tomatoes,
        Sudden wilting and total blackened collapse of foliage
      ],
      remedies: {
        organic: [
          Rogue and safely bag/dispose of infected plants immediately,
          Apply bio-fungicides with Bacillus subtilis,
          Avoid working with wet plants to prevent spreading spores
        ],
        chemical: [
          Metalaxyl + Mancozeb (2.5g/L) systemic spray,
          Fenamidone 10% + Mancozeb 50% WG (2.5g/L),
          Ametoctradin + Dimethomorph (1.5ml/L)
        ],
        prevention: [
          Plant certified resistant varieties (e.g. Defiant, Mountain Magic),
          Avoid planting tomatoes adjacent to potato fields,
          Provide wide spacing (75-90 cm) between vines
        ]
      }
    },
    Septoria Leaf Spot: {
      pathogen: Septoria lycopersici,
      isHealthy: false,
      severity: Moderate,
      description: Destructive fungal foliar disease producing numerous small circular lesions with dark borders and gray centers.,
      causes: Warm temperatures (20-25°C), high humidity, overhead watering.,
      symptoms: [
        Numerous small circular spots (2-3mm) with dark brown borders and pale grey centers,
        Tiny black fruiting specks (pycnidia) visible within spot centers,
        Progressive upward defoliation exposing fruit to sunscald
      ],
      remedies: {
        organic: [
          Prune infected lower leaves as soon as first spots appear,
          Apply potassium bicarbonate or liquid copper fungicides,
          Sterilize pruning shears with 70% isopropyl alcohol
        ],
        chemical: [
          Chlorothalonil 75 WP (2g/L) or Mancozeb 75 WP (2g/L),
          Pyraclostrobin or Azoxystrobin (1ml/L)
        ],
        prevention: [
          2-3 year crop rotation away from solanaceous species,
          Deep bury crop residue at the end of the season,
          Avoid overhead sprinkler irrigation
        ]
      }
    },
    Healthy: {
      pathogen: N/A (Optimal Health),
      isHealthy: true,
      severity: None,
      description: Vigorous tomato vine showing strong apical growth, deep green foliage, and healthy flowering.,
      causes: Optimal sunlight, balanced fertility, and controlled hydration.,
      symptoms: [
        Deep green lush foliage with healthy serrated margins,
        Firm petioles and sturdy central vine growth,
        Normal flower bud formation without chlorosis
      ],
      remedies: {
        organic: [
          Maintain organic feeding with seaweed/compost extract,
          Apply regular mulch replenishment
        ],
        chemical: [
          No chemical fungicide required
        ],
        prevention: [
          Maintain 6-8 hours of direct daily sunlight,
          Ensure balanced soil calcium and magnesium levels
        ]
      }
    }
  },
  apple: {
    Apple Scab: {
      pathogen: Venturia inaequalis,
      isHealthy: false,
      severity: Severe,
      description: Widespread fungal disease causing olive-green to velvety black scabs on leaves and fruit.,
      causes: Overwintering in fallen leaves, prolonged springtime leaf wetness at 15-24°C.,
      symptoms: [
        Olive-green to velvety brown circular spots on upper leaf surfaces,
        Leaves becoming puckered, twisted, and dropping prematurely,
        Fruit developing dark corky, cracked, scabby lesions
      ],
      remedies: {
        organic: [
          Rake and destroy fallen leaves in autumn to eliminate overwintering spores,
          Apply sulfur-based or copper soap sprays during early bud break,
          Prune tree canopy to maximize sun penetration and air circulation
        ],
        chemical: [
          Captan 50 WP (2.5g/L) or Mancozeb 75 WP (2g/L) as protective sprays,
          Myclobutanil 10 WP (1g/L) or Difenoconazole 25 EC (0.5ml/L) for curative action
        ],
        prevention: [
          Plant scab-resistant cultivars (e.g. Enterprise, Liberty, Honeycrisp),
          Apply 5% urea spray to fallen orchard leaves in late autumn
        ]
      }
    },
    Black Rot: {
      pathogen: Botryosphaeria obtusa,
      isHealthy: false,
      severity: Severe,
      description: Fungal disease causing frog-eye leaf spots, limb cankers, and firm mummified black fruit rot.,
      causes: Dead wood, mummified apples, warm humid weather (24-27°C).,
      symptoms: [
        Frog-eye leaf spots: purple specks expanding to spots with tan centers and purple borders,
        Sunken reddish-brown cankers on branches and limbs,
        Fruit developing brown rot with concentric black rings, turning into dry mummies
      ],
      remedies: {
        organic: [
          Prune out dead wood and cankered branches 6 inches below infected zone,
          Remove and safely dispose of all mummified fruit remaining on trees,
          Lime sulfur sprays during dormant season
        ],
        chemical: [
          Thiophanate-methyl 70 WP (1g/L) or Captan 50 WP (2g/L),
          Flint (Trifloxystrobin) or Pristine (Pyraclostrobin + Boscalid)
        ],
        prevention: [
          Maintain tree vigor through balanced fertilization and pest control,
          Disinfect pruning tools between cuts
        ]
      }
    },
    Cedar Apple Rust: {
      pathogen: Gymnosporangium juniperi-virginianae,
      isHealthy: false,
      severity: Moderate,
      description: Heteroecious rust fungus requiring both apple trees and Eastern red cedar/juniper to complete its life cycle.,
      causes: Proximity to juniper trees, spring rain releasing spores from cedar galls.,
      symptoms: [
        Bright yellow-orange circular spots on upper apple leaf surfaces,
        Spots enlarging and developing reddish borders with tiny black dots,
        Underside of spots forming tube-like fringe structures (aecia),
        Early summer defoliation and dwarfed fruit
      ],
      remedies: {
        organic: [
          Remove nearby wild juniper/cedar shrubs within 500m radius if possible,
          Prune and remove galls from ornamental junipers during late winter,
          Apply sulfur sprays beginning at pink bud stage
        ],
        chemical: [
          Myclobutanil 10 WP (1g/L) or Mancozeb 75 WP (2g/L),
          Propiconazole 25 EC (1ml/L) applied at tight cluster through petal fall
        ],
        prevention: [
          Choose rust-resistant apple cultivars (e.g. Redfree, William's Pride),
          Avoid planting apple orchards adjacent to cedar windbreaks
        ]
      }
    },
    Healthy: {
      pathogen: N/A (Optimal Health),
      isHealthy: true,
      severity: None,
      description: Lush apple foliage with deep green color, strong shoot growth, and clean fruit spur development.,
      causes: Regular orchard hygiene, balanced fertility, and proactive canopy pruning.,
      symptoms: [
        Glossy, deep green leaves without rust spots, scabs, or mildew,
        Clean bark and active branch terminal growth,
        Healthy flower blossoms and fruit set
      ],
      remedies: {
        organic: [
          Apply dormant oil spray in early spring for pest and scale suppression,
          Maintain compost mulching around tree drip line
        ],
        chemical: [
          No fungicide required
        ],
        prevention: [
          Perform annual winter pruning for optimal sun penetration and airflow,
          Maintain adequate boron and zinc micronutrient balance
        ]
      }
    }
  }
};
