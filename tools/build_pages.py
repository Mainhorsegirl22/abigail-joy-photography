#!/usr/bin/env python3
"""The Pine Hill pages, built on phkit.

  python3 build_pages.py <page> data   -> _elementor_data JSON
  python3 build_pages.py <page> css    -> the page stylesheet
  python3 build_pages.py <page> index  -> class -> element ids

Real figures only. Price and deposit came from Abigail. Freda's health results
and AKC number are lifted from her own Females page, with the original
certificate links kept so a buyer can open the paperwork. Anything nobody has
told me is written with fill(), which renders as a visible blank.
"""
import sys
from phkit import (start, section, con, row, w, h, p, ul, dl, btn, img, rule,
                   fill, pill, hero, sec, head, split, col, trio, quad, card,
                   stat, steps, faq, cta, emit, IMG, INDEX)

DOCS = "https://www.pinehillgermanshepherds.com/wp-content/uploads/2025/04"
FREDA = {
    "name": "Freda von Stephanitz",
    "dob": "1 July 2023",
    "akc": "DN76717801",
    "pedigree": f"{DOCS}/Fredas-Pedigree-scaled-1.jpeg",
    "hips": f"{DOCS}/Freda-Pennhip-Results-3.pdf",
    "elbows": f"{DOCS}/FREDA-VON-STEPHANITZ-ELBOW-10_18_2024-ELBOW.pdf",
    "heart": f"{DOCS}/Screenshot-2025-01-15-174147.png",
    "eyes": f"{DOCS}/OFA-Case-249JFB.pdf",
}


def link(text, url):
    return f"<a href='{url}' target='_blank' rel='noopener'>{text}</a>"


# ============================================================ PUPPIES
def puppies():
    start("pup")

    d = [hero("AKC Working-Line German Shepherd Puppies",
              "raised in our home, not a kennel", "puppies", ypos=60,
              button=("Join the Waiting List", "/reserve-a-puppy/"))]

    # --- what's happening right now, at the top, because it's why they came
    d.append(sec([con([
        pill("Waiting list open", "open"),
        h("Next Litter — Late Fall 2026"),
        p("Freda is expecting in late fall. Reservations are taken in the order "
          "deposits are received, and puppies are matched to families at six weeks.",
          "ph-lede"),
        btn("Join the Waiting List", "/reserve-a-puppy/"),
    ], "ph-narrow")], "status", tone="linen", tight=True))

    # --- the offer, plainly
    d.append(sec([
        head("what you get", "Every Puppy Leaves Here With",
             "No surprises and nothing held back — the same four things on every "
             "puppy, every litter."),
        trio([
            card([h("Health-tested parents", tag="h3"),
                  p("Both parents screened for hips, elbows, eyes and heart before "
                    "breeding, plus a full genetic panel. The certificates are "
                    "published on this site — you can read them yourself.")]),
            card([h("A written health guarantee", tag="h3"),
                  p("In writing, in the sales contract, signed before your puppy "
                    "goes home. You will know exactly what is covered.")]),
            card([h("AKC registration", tag="h3"),
                  p("Full AKC papers. Freda is registered under "
                    f"{FREDA['akc']}, and her pedigree is available to read.")]),
        ]),
    ], "offer", tone="white"))

    # --- price: she gave me these figures, so they are stated plainly
    d.append(sec([split(
        col([
            p("what it costs", "ph-script"),
            h("Price and Deposit"),
            rule(),
            dl([("Puppy", "$3,000"),
                ("Deposit", "$500, applied to the price"),
                ("Balance due", "Before go-home day at eight weeks")]),
            p("The deposit holds your place in line. Puppies are matched to "
              "families at six weeks, once temperaments are clear.", "ph-measure"),
            p(f"Also included: {fill('vaccinations, microchip, vet certificate — confirm')}",
              "ph-measure"),
            btn("Reserve a Puppy", "/reserve-a-puppy/"),
        ]),
        img("portrait"),
    )], "price", tone="linen"))

    # --- how they are raised
    d.append(sec([
        head("how they're raised", "The First Nine Weeks",
             "Every puppy goes through the same programme, from the day they are "
             "born until the day they go home."),
        steps([
            ("Days 3–16", "Early Neurological Stimulation",
             "A short daily handling routine that builds tolerance to stress and "
             "handling before the eyes are even open."),
            ("Weeks 3–4", "Early Scent Introduction",
             "A new scent every day. This is the foundation under the detection and "
             "search work our dogs go on to do."),
            ("Weeks 5–7", "Puppy Culture",
             "Problem-solving, novel surfaces, crate introduction, manding, and "
             "recovery from small startles."),
            ("Week 8", "Go-home day",
             "Crate-started, handled daily, and used to the noise of a working "
             "family home."),
        ]),
        con([btn("More About Puppy Culture", "/puppy-culture/", "ph-ghost")], "ph-cta__in"),
    ], "raised", tone="white"))

    # --- K9 Scholars, marked as the example it is
    d.append(sec([split(
        img("scholars"),
        col([
            p("k9 scholars", "ph-script"),
            h("Taking Training Further"),
            rule(),
            p("Our own five-week programme, run after the Puppy Culture weeks for "
              "families who want a head start. Puppies learn advanced manners and "
              "meet situations most puppies do not see until much later.",
              "ph-measure"),
            ul(["Sit, stay, come and leash work", "Crate training",
                "Manding — the automatic sit", "Food manners",
                "Advanced socialisation", "Scent detection games",
                "Confidence building", "Manners in public"]),
            p(f"Price and dates: {fill('to be confirmed')}", "ph-measure"),
            btn("Learn More", "/k9-scholars/", "ph-ghost"),
        ]),
    )], "schol", tone="linen"))

    # --- questions
    d.append(sec([
        head("before you ask", "Questions We Get Every Litter", centred=True),
        faq([
            ("How do I get on the waiting list?",
             "Fill in the application, we talk, and a $500 deposit holds your place. "
             "Places are filled in the order deposits arrive."),
            ("How are puppies matched to families?",
             "At six weeks, once temperaments have settled. We match on temperament "
             "and on what you want the dog for, not on first-come pick of the litter. "
             "This is the single biggest thing that makes a placement work."),
            ("Can I choose my puppy myself?",
             "We will talk it through with you, and we listen. But we have watched "
             "these puppies every day for six weeks and you will have met them "
             "briefly, so we will tell you honestly if we think a different puppy "
             "suits you better."),
            ("Do you ship puppies?",
             "Puppies can be collected from our home in Garland. For families who "
             "cannot make the trip we offer delivery — ask and we will work it out."),
            ("What if I change my mind?",
             f"The deposit terms are in the sales contract. {fill('refundable or not — confirm')}"),
            ("What is a working-line German Shepherd like to live with?",
             "Busy. These are dogs bred to work, with real drive and real stamina. "
             "They are wonderful family dogs for families who give them a job. They "
             "are a poor choice for a quiet house with no time for training."),
        ]),
    ], "faq", tone="white", tight=True))

    d.append(cta("Ready to Start?",
                 "Tell us about your family and what you are looking for. "
                 "We answer every enquiry ourselves.",
                 "Join the Waiting List", "/reserve-a-puppy/", image_key="litter_band"))
    return d


# ============================================================ LITTERS
def litters():
    start("lit")

    d = [hero("Current and Upcoming Litters", "reserve your puppy",
              "litter_band", ypos=62, tall=False)]

    d.append(sec([
        head("what's planned", "Late Fall 2026",
             "We plan one litter at a time, so that every puppy gets the same "
             "attention. This is everything currently planned."),
        con([split(
            img("puppies", "ph-frame"),
            col([
                pill("Waiting list open", "open"),
                h("Freda × Barley — Late Fall 2026", tag="h3"),
                dl([("Dam", FREDA["name"]),
                    ("Sire", "Barley Fatymona of Spodnick's K9"),
                    ("Sire rating", "SG · IGP3 · Czech import"),
                    ("Sire health", "Hips A · Elbows 0/0 · DM N/N"),
                    ("Expected", "Late fall 2026"),
                    ("Puppies expected", fill("estimate")),
                    ("Colours", fill("sable, bi-colour?")),
                    ("Price", "$3,000 · $500 deposit")]),
                p("Reservations are taken in the order deposits are received. "
                  "Puppies are matched to families at six weeks.", "ph-measure"),
                btn("Reserve a Puppy", "/reserve-a-puppy/"),
            ]),
        )], "ph-litter"),
    ], "current", tone="white"))

    d.append(sec([
        head("the parents", "Who They Come From", centred=True),
        row([
            card([img("freda", "ph-frame ph-frame--sq"),
                  h(FREDA["name"], tag="h3"),
                  p("Dam · dark sable · search and rescue", "ph-role"),
                  dl([("Hips", link("Good", FREDA["hips"])),
                      ("Elbows", link("Good", FREDA["elbows"])),
                      ("Heart", link("Normal", FREDA["heart"])),
                      ("Eyes", link("Normal", FREDA["eyes"])),
                      ("Genetics", "Clear")]),
                  btn("Read Her Pedigree", FREDA["pedigree"], "ph-ghost")]),
            card([img("working", "ph-frame ph-frame--sq"),
                  h("Barley Fatymona", tag="h3"),
                  p("Sire · Czech import · at stud with Spodnick's K9", "ph-role"),
                  dl([("Rating", "SG"), ("Title", "IGP3"),
                      ("Hips", "A"), ("Elbows", "0/0"), ("DM", "N/N")]),
                  p(f"Photograph: {fill('a photo of Barley would be better here')}",
                    "ph-note")]),
        ], "ph-split"),
    ], "parents", tone="linen"))

    d.append(sec([
        head("previously", "Past Litters",
             "Puppies from earlier litters, now living and working with their families."),
        quad([con([img(k, "ph-frame ph-frame--sq"), p(c, "ph-role")], "ph-col")
              for k, c in [("rangley1", "Spring 2026"), ("rangley3", "Autumn 2025"),
                           ("rangley5", "Spring 2025"), ("rangley7", "Autumn 2024")]]),
        p(f"Dates above are {fill('examples — give me the real litter dates')}",
          "ph-note"),
    ], "past", tone="white"))

    d.append(cta("Nothing Available Right Now?",
                 "Join the waiting list and you will hear about the next litter "
                 "before it is announced anywhere else.",
                 "Join the Waiting List", "/reserve-a-puppy/", image_key="band2"))
    return d


EXTRA = """
.ph-role p{font-size:10.5px!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:var(--brass)!important}
.ph-note p{font-size:12.5px!important;color:var(--brass)!important}
.ph-litter{max-width:var(--wrap)!important;margin-inline:auto!important;padding:0!important;
 gap:0!important}
.ph-facts a{color:var(--espresso);text-decoration:underline;text-underline-offset:3px;
 text-decoration-color:var(--brass)}
.ph-facts a:hover{color:var(--brass)}
.ph-card .ph-facts{width:100%}
.ph-card .elementor-button{margin-top:6px}
"""

PAGES = {"puppies": puppies, "litters": litters}

if __name__ == "__main__":
    name, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "data")
    data = PAGES[name]()
    j, c = emit(data, EXTRA)
    if mode == "data":
        sys.stdout.write(j)
    elif mode == "css":
        sys.stdout.write(c)
    elif mode == "index":
        import json
        sys.stdout.write(json.dumps(INDEX, indent=1))
