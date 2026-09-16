from django.core.management.base import BaseCommand
from safety_app.models import Department, SafetyTopic, Employee, AssessmentAttempt, AnswerLog


class Command(BaseCommand):
    help = "Seeds initial plant departments, safety standards, and demo profiles."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Tata Steel Safety Data...")

        # 1. Departments
        departments_data = [
            {
                "code": "BF-01",
                "name": "Blast Furnace & Hot Metal",
                "description": "Iron production operations with high thermal and blast furnace gas hazards.",
                "primary_hazards": "Toxic Gas (CO), Liquid Iron Splash (1450°C), High Radiant Heat, Pressure Vessels"
            },
            {
                "code": "SMS-02",
                "name": "Steel Melting Shop (SMS / LD Shop)",
                "description": "Oxygen steelmaking, refining, continuous casting, and liquid steel ladle handling.",
                "primary_hazards": "Molten Slag Explosions, Heavy Overhead Cranes, Torpedo Ladle Derailment"
            },
            {
                "code": "RM-03",
                "name": "Hot & Cold Rolling Mills",
                "description": "Transformation of steel slabs/billets into sheets, coils, and structural sections.",
                "primary_hazards": "Pinch Points, High-Speed Flying Coils, Hydraulic High Pressure, Acid Pickling"
            },
            {
                "code": "CO-04",
                "name": "Coke Ovens & By-Products",
                "description": "Coal carbonization, battery top operations, and chemical by-product recovery.",
                "primary_hazards": "Carcinogenic Coal Tar Pitch, Benzene Vapors, Flammable Gases, Fall from Heights"
            },
            {
                "code": "ELEC-05",
                "name": "Electrical Substations & Distribution",
                "description": "High voltage distribution, switchgear maintenance, and zero-energy lockout (LOTOTO).",
                "primary_hazards": "Arc Flash (33kV/6.6kV), Electrocution, Stored Capacitive Energy, Transformer Explosions"
            },
            {
                "code": "LOG-06",
                "name": "Plant Logistics & Heavy Mobile Equipment",
                "description": "Internal rail movement, heavy trailers, coil transport, and pedestrian pathway management.",
                "primary_hazards": "Locomotive Collisions, Forklift Blind Spots, Dumper Rollover, Pedestrian Pinch Zones"
            },
        ]

        dept_objs = {}
        for d in departments_data:
            obj, _ = Department.objects.get_or_create(
                code=d["code"],
                defaults={
                    "name": d["name"],
                    "description": d["description"],
                    "primary_hazards": d["primary_hazards"]
                }
            )
            dept_objs[d["code"]] = obj

        # 2. Safety Topics (TSS-01 to TSS-06)
        topics_data = [
            {
                "topic_id": "ppe",
                "title": "Personal Protective Equipment (PPE)",
                "sop_code": "TSS-01",
                "sop_name": "Tata Steel Standard: Mandatory PPE & Specialized Gear",
                "description": "Proper inspection, donning, maintenance, and zero-tolerance usage of helmets, safety shoes, flame-retardant suits, and respirator units.",
                "icon": "shield"
            },
            {
                "topic_id": "fire-gas",
                "title": "Fire Safety & Toxic Gas Hazards (CO / Benzene)",
                "sop_code": "TSS-02",
                "sop_name": "Tata Steel Standard: Gas Monitoring & Emergency Evacuation",
                "description": "CO gas leak detection, personal multi-gas monitors, explosive limit protocols, SCBA usage, and assembly points.",
                "icon": "flame"
            },
            {
                "topic_id": "loto",
                "title": "Electrical Safety & LOTO (LOTOTO)",
                "sop_code": "TSS-03",
                "sop_name": "Tata Steel Standard: Isolation of Hazardous Energy (LOTOTO)",
                "description": "Lock-out, Tag-out, Try-out procedure. Electrical isolation, arc flash PPE, and zero-energy verification before machine intervention.",
                "icon": "zap"
            },
            {
                "topic_id": "heights",
                "title": "Working at Heights & Confined Spaces",
                "sop_code": "TSS-04",
                "sop_name": "Tata Steel Standard: Fall Protection & Tank Entry Clearance",
                "description": "Full-body harnesses, 100% tie-off, scaffolding green tags, oxygen testing (19.5% - 23.5%), and continuous hole-watch supervision.",
                "icon": "building"
            },
            {
                "topic_id": "molten-metal",
                "title": "Molten Metal & Hot Heavy Cranes",
                "sop_code": "TSS-05",
                "sop_name": "Tata Steel Standard: Hot Metal Handling & Overhead Crane Safety",
                "description": "Exclusion red zones, ladle crane wire rope inspections, slag pit water moisture prevention, and radiant shielding.",
                "icon": "alert-triangle"
            },
            {
                "topic_id": "emergency",
                "title": "Emergency Response & Golden Hour Protocols",
                "sop_code": "TSS-06",
                "sop_name": "Tata Steel Standard: Plant Disaster Management & Medical First Aid",
                "description": "Plant siren codes, chemical splash deluge showers, burns first aid, automated external defibrillators (AED), and incident escalation.",
                "icon": "heart"
            }
        ]

        for t in topics_data:
            SafetyTopic.objects.get_or_create(
                topic_id=t["topic_id"],
                defaults={
                    "title": t["title"],
                    "sop_code": t["sop_code"],
                    "sop_name": t["sop_name"],
                    "description": t["description"],
                    "icon": t["icon"]
                }
            )

        # 3. Demo Employees
        demo_employees = [
            {"emp_id": "TS-84920", "name": "Ramesh Kumar", "dept_code": "BF-01"},
            {"emp_id": "TS-61024", "name": "Priya Sharma", "dept_code": "SMS-02"},
            {"emp_id": "TS-93411", "name": "Amit Verma", "dept_code": "ELEC-05"},
        ]

        for emp in demo_employees:
            e_obj, created = Employee.objects.get_or_create(
                emp_id=emp["emp_id"],
                defaults={
                    "name": emp["name"],
                    "department": dept_objs[emp["dept_code"]]
                }
            )

            # Seed initial attempts for Ramesh Kumar to showcase the weak area detection feature right away!
            if created and emp["emp_id"] == "TS-84920":
                # Weak PPE attempt (Score 10/30 = 33%)
                att1 = AssessmentAttempt.objects.create(
                    employee=e_obj,
                    topic_title="Personal Protective Equipment (PPE)",
                    difficulty="beginner",
                    is_remediation=False,
                    score=10,
                    max_score=30,
                    percentage=33
                )
                AnswerLog.objects.create(
                    attempt=att1,
                    topic_id="ppe",
                    scenario_context="Blast Furnace Cast House Gate",
                    question_text="Helmet has a hairline crack. What to do?",
                    chosen_option="A",
                    chosen_text="Enter anyway because the shell is mostly intact.",
                    correct_option="B",
                    correct_text="Immediately replace the helmet before entering.",
                    is_correct=False,
                    explanation="Any crack destroys the structural integrity of the helmet.",
                    consequence="Dropping 20mm bolt can shatter helmet and cause fatal trauma.",
                    sop_reference="TSS-01 §4.3"
                )
                AnswerLog.objects.create(
                    attempt=att1,
                    topic_id="ppe",
                    scenario_context="Ladle Furnace Deck",
                    question_text="Visor is covered in splatter.",
                    chosen_option="A",
                    chosen_text="Tilt visor up to see underneath.",
                    correct_option="B",
                    correct_text="Step into control cabin and replace visor.",
                    is_correct=False,
                    explanation="Tilting visor exposes eyes to irreversible thermal radiation.",
                    consequence="Direct IR radiation causes cataracts and corneal burns.",
                    sop_reference="TSS-01 §8.1"
                )
                AnswerLog.objects.create(
                    attempt=att1,
                    topic_id="ppe",
                    scenario_context="Hot Strip Mill Perimeter",
                    question_text="Footwear requirement in heavy mills.",
                    chosen_option="B",
                    chosen_text="Steel-toe safety shoes with puncture-resistant midsole.",
                    correct_option="B",
                    correct_text="Steel-toe safety shoes with puncture-resistant midsole.",
                    is_correct=True,
                    explanation="Complies with IS 15298 safety shoe standard.",
                    consequence="Unrated shoes leave feet defenseless against steel crushing.",
                    sop_reference="TSS-01 §5.0"
                )

                # Strong Gas safety attempt (Score 30/30 = 100%)
                att2 = AssessmentAttempt.objects.create(
                    employee=e_obj,
                    topic_title="Fire Safety & Toxic Gas Hazards",
                    difficulty="intermediate",
                    is_remediation=False,
                    score=30,
                    max_score=30,
                    percentage=100
                )
                AnswerLog.objects.create(
                    attempt=att2,
                    topic_id="fire-gas",
                    scenario_context="BF Gas Cleaning Plant",
                    question_text="CO detector alarms at 35 PPM.",
                    chosen_option="B",
                    chosen_text="Immediately evacuate upwind.",
                    correct_option="B",
                    correct_text="Immediately evacuate upwind.",
                    is_correct=True,
                    explanation="CO binds to hemoglobin rapidly, upwind evacuation is life saving.",
                    consequence="Hypoxia and sudden loss of consciousness within minutes.",
                    sop_reference="TSS-02 §3.1"
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Tata Steel safety data and demo profiles!"))
