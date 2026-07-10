"""
Base de connaissances maintenance prédictive.

Chaque défaut possède une signature basée sur
les grandeurs physiques du moteur.
"""


FAULT_KNOWLEDGE = {


    "Bearing Wear": {

        "description":
            "Usure des roulements",

        "symptoms": {

            "wear": {
                "threshold": 30,
                "score": 35
            },

            "vibration": {
                "threshold": 0.8,
                "score": 30
            },

            "temperature": {
                "threshold": 70,
                "score": 15
            },

            "current": {
                "threshold": 10,
                "score": 10
            },

            "speed": {
                "threshold": 1450,
                "operator": "less",
                "score": 10
            }

        }

    },


    "Rotor Misalignment": {

        "description":
            "Désalignement mécanique du rotor",

        "symptoms": {

            "misalignment": {

                "threshold": 20,
                "score": 40

            },

            "vibration": {

                "threshold": 1,
                "score": 30

            },

            "speed": {

                "threshold": 1450,
                "operator": "less",
                "score": 15

            },

            "temperature": {

                "threshold": 65,
                "score": 15

            }

        }

    },


    "Cooling Failure": {

        "description":
            "Défaillance du système de refroidissement",

        "symptoms": {


            "temperature": {

                "threshold": 80,
                "score": 50

            },


            "current": {

                "threshold": 12,
                "score": 20

            },


            "load": {

                "threshold": 70,
                "score": 15

            },


            "wear": {

                "threshold": 40,
                "score": 15

            }

        }

    },


    "Motor Overload": {

        "description":
            "Surcharge mécanique du moteur",

        "symptoms": {


            "load": {

                "threshold": 80,
                "score": 40

            },


            "current": {

                "threshold": 12,
                "score": 25

            },


            "torque": {

                "threshold": 18,
                "score": 20

            },


            "temperature": {

                "threshold": 70,
                "score": 15

            }

        }

    },


    "Electrical Fault": {

        "description":
            "Défaut électrique",

        "symptoms": {


            "current": {

                "threshold": 15,
                "score": 45

            },


            "temperature": {

                "threshold": 75,
                "score": 20

            },


            "speed": {

                "threshold": 1400,
                "operator": "less",
                "score": 20

            },


            "vibration": {

                "threshold": 0.9,
                "score": 15

            }

        }

    },


    "Power Loss": {

        "description":
            "Perte d'alimentation moteur",

        "symptoms": {


            "current": {

                "threshold": 1,
                "operator": "less",
                "score": 60

            },


            "speed": {

                "threshold": 300,
                "operator": "less",
                "score": 40

            }

        }

    }

}