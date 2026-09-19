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
from phkit import (start, section, con, row, w, h, p, ul, dl, btn, img, rule, form,
                   fill, pill, hero, sec, head, split, col, trio, quad, card,
                   stat, steps, faq, cta, emit, pin, gform, IMG, INDEX)

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


RANGELEY = {
    "name": "Ledger Bei Mackenzie von Franzosisches Haus",
    "call": "Rangeley",
    "akc": "DN77163902",
}


def link(text, url):
    """An outside link - a PDF, a registry, a health result. Opens in its own
    tab so the reader does not lose the page they were on."""
    return f"<a href='{url}' target='_blank' rel='noopener'>{text}</a>"


def here(text, path):
    """A link to another page of this site. Stays in the same tab."""
    return f"<a href='{path}'>{text}</a>"


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
                  p("Genetic hip and elbow dysplasia covered for twenty-four "
                    "months, plus a three-day vet check window. It is in the "
                    "contract you sign before your puppy goes home \u2014 you can "
                    "read the whole thing first.")]),
            card([h("AKC registration", tag="h3"),
                  p("AKC papers on Limited Registration \u2014 a pet home, not "
                    "breeding or show rights. Full Registration is possible, but "
                    "only by written agreement beforehand and for an additional "
                    f"fee. Freda is registered under {FREDA['akc']}.")]),
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
            ul(["Wormed at four, six and eight weeks",
                "First vaccination from a licensed vet, with written proof",
                "Vet-checked before pickup",
                "AKC papers, Limited Registration"], "ph-list ph-list--one"),
            p("The balance is due in full at pickup, in certified funds or cash. "
              "Personal cheques are not accepted at pickup.", "ph-measure"),
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
             "The $500 deposit is non-refundable. If the balance is not paid and "
             "the puppy not collected within fourteen days of the agreed date, "
             "the reservation ends and the puppy is offered to the next family. "
             "Those terms are set out in the " +
             here("sales contract", "/sales-contract-new/") +
             ", which you can read in full before you pay anything."),
            ("Is there a health guarantee?",
             "Yes, in writing. Debilitating genetic hip or elbow dysplasia is "
             "covered for twenty-four months from pickup, on proof from your vet. "
             "The remedy is a replacement puppy from a future litter rather than "
             "a refund. There is also a three-day window for a vet check, and if "
             "your vet certifies the puppy unfit for sale you can return it."),
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
# CAUTION: Abigail replaced the litter-card image in the Elementor editor with
# a "Litter A" announcement poster. That change lives in _elementor_data, not
# here, so regenerating this page and pushing the data would overwrite it. Ask
# her before pushing litters data again; the stylesheet is safe to push.
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
                h(f"Freda \u00d7 {RANGELEY['call']} \u2014 Late Fall 2026", tag="h3"),
                dl([("Dam", FREDA["name"]),
                    ("Sire", RANGELEY["name"]),
                    ("Expected", "Late fall 2026"),
                    ("Puppies expected", fill("estimate")),
                    ("Colours", fill("sable, bi-colour?")),
                    ("Registration", "AKC, Limited"),
                    ("Price", "$3,000 \u00b7 $500 deposit")]),
                p("Reservations are taken in the order deposits are received. "
                  "Puppies are matched to families at six weeks, once their "
                  "temperaments are clear.", "ph-measure"),
                btn("Reserve a Puppy", "/reserve-a-puppy/"),
            ]),
        )], "ph-litter"),
    ], "current", tone="white"))

    # Both parents, with every result printed and the paperwork linked where
    # she has published it. This is the page a serious buyer actually reads.
    d.append(sec([
        head("the parents", "Health Testing, In Full",
             "Every result below is on file. Freda's certificates open in a new "
             "tab. Rangeley's OFA results are searchable on his registration "
             "number."),
        row([
            card([img("freda", "ph-frame ph-frame--sq"),
                  h(FREDA["name"], tag="h3"),
                  p("Dam \u00b7 dark sable \u00b7 search and rescue", "ph-role"),
                  dl([("AKC", FREDA["akc"]),
                      ("Hips", link("Good", FREDA["hips"])),
                      ("Elbows", link("Good", FREDA["elbows"])),
                      ("Heart", link("Normal", FREDA["heart"])),
                      ("Eyes", link("Normal", FREDA["eyes"])),
                      ("Genetics", "Clear")]),
                  btn("Read Her Pedigree", FREDA["pedigree"], "ph-ghost")]),
            card([img("rangeley1", "ph-frame ph-frame--sq"),
                  h(RANGELEY["name"], tag="h3"),
                  p(f"Sire \u00b7 called {RANGELEY['call']}", "ph-role"),
                  dl([("AKC", RANGELEY["akc"]),
                      ("Hips", "OFA Good"),
                      ("Elbows", "OFA Normal"),
                      ("Heart", "OFA Advanced Echocardiogram, Normal"),
                      ("Eyes", "OFA CAER, Normal"),
                      ("Genetics", "Embark, Clear")]),
                  p("An advanced echocardiogram is a step beyond the basic "
                    "cardiac exam most breeders stop at.", "ph-note")]),
        ], "ph-split"),
    ], "parents", tone="linen"))

    d.append(sec([
        head("the sire", RANGELEY["call"],
             "A dark sable working-line male with a full OFA panel behind him."),
        quad([img(k, "ph-frame ph-frame--sq")
              for k in ("rangeley2", "rangeley3", "rangeley5", "rangeley7")]),
    ], "sire", tone="white"))

    d.append(cta("Nothing Available Right Now?",
                 "Join the waiting list and you will hear about the next litter "
                 "before it is announced anywhere else.",
                 "Join the Waiting List", "/reserve-a-puppy/", image_key="band2"))
    return d


# ============================================================ SALES CONTRACT
# Her contract, reproduced. The wording of the terms is hers and is not
# reworded here - only laid out so it can be read on a phone without pinching.
def contract():
    start("con")

    # No photograph and no summary: Abigail asked for the contract itself on a
    # white page and nothing else. Title, clauses and signature are one column
    # inside one section, so nothing sits in a band of its own and the page
    # reads the way a contract on paper does.
    d = []

    body = [
        ("1. Price and payment",
         "The price is the amount agreed at reservation. A deposit holds the "
         "puppy and is non-refundable. The balance is due in full at pickup, "
         "before the puppy leaves, by cash or certified funds."),
        (None,
         "If the Buyer has not paid the balance and collected the puppy within "
         "14 days of the agreed date, and has made no other written "
         "arrangement, this Agreement ends, the deposit is kept, and the Seller "
         "may resell the puppy."),
        ("2. Health and vaccination",
         "Sire and dam are health-tested. Puppies are raised in-home and wormed "
         "before going home."),
        (None,
         "At 7 weeks of age, or before the puppy leaves our premises, it "
         "receives its first vaccination. This is the first in a series \u2014 the "
         "Buyer continues the schedule with their own veterinarian. The "
         "vaccination record is handed over at pickup, and the puppy is "
         "believed to be in good health at that time."),
        ("3. Vet check and return",
         "The Buyer must have the puppy examined by their own veterinarian "
         "within 3 days of coming home. If that vet certifies in writing that "
         "the puppy is unfit for sale, the Buyer may return it, in the same "
         "condition as sold, within those same 3 days, for a refund of the "
         "purchase price less the deposit. Travel and other costs are not "
         "covered. After that window the Seller is not responsible for "
         "conditions that develop later, except under the guarantee below."),
        ("4. Genetic health guarantee",
         "The Seller guarantees the puppy against debilitating genetic hip or "
         "elbow dysplasia for 24 months from pickup. To qualify, the dog must "
         "have written veterinary proof, must have been kept at a sensible "
         "weight and activity level, and must not have been bred. The Seller "
         "will replace the puppy from a future litter when one is available. "
         "There is no cash refund. Injury, diet, exercise and non-genetic "
         "conditions are not covered."),
        ("5. Buyer\u2019s responsibilities",
         "The Buyer will keep the dog safe, well fed, properly exercised and "
         "under veterinary care, and will not neglect or mistreat it."),
        ("6. Seller\u2019s responsibilities",
         "Before pickup the Seller worms, vet-checks and vaccinates the puppy "
         "as described above, and provides AKC papers showing Limited "
         "Registration unless otherwise agreed in writing."),
        ("7. General terms",
         "Once the Buyer takes the puppy home, the Buyer is responsible for the "
         "dog and releases the Seller from liability for anything the dog does "
         "to any person or property."),
        (None,
         "This Agreement is governed by Maine law. If either party goes to law "
         "to enforce it, the losing party pays the winner\u2019s costs. If any "
         "part of this Agreement cannot be enforced, the rest still stands."),
        (None,
         "This is the entire agreement between the parties, binding on their "
         "heirs and successors, and may be signed electronically."),
    ]
    # A masthead, not a dropped-in title: who the agreement is with, what it is,
    # and where it is made, closed by a rule across the column the way a piece of
    # headed paper is.
    blocks = [con([p("Pine Hill German Shepherds", "ph-script ph-mast__co"),
                   h("Puppy Sales Contract", "ph-title", tag="h1"),
                   p("This is not to intimidate anybody, but just to keep both "
                     "parties safe in the process. If you have any questions "
                     "about our sales contract, please don\u2019t hesitate to "
                     "reach out and ask us.", "ph-mast__note")],
                  "ph-mast"),
              p("Pine Hill German Shepherds (\u201cSeller\u201d) agrees to sell the "
                "purebred German Shepherd puppy described below to the Buyer, on "
                "the terms below. The puppy is AKC-registered under Limited "
                "Registration \u2014 pet only, no breeding or show rights. Buyers "
                "wanting Full Registration and breeding rights must contact the "
                "Seller in advance for approval and an additional fee.",
                "ph-lede")]
    # The clauses are set on a grid rather than run together: the number and the
    # name of the clause hold a rail on the left, the wording sits in its own
    # column on the right. A numbered heading typed into the prose is a list; a
    # rail is a contract you can find your way around.
    for heading, para in body:
        if heading:
            num, _, title = heading.partition(". ")
            blocks.append(row([
                con([p(f"{int(num):02d}", "ph-cnum"),
                     h(title, "ph-ctitle", tag="h3")], "ph-crow__n"),
                con([p(para, "ph-terms")], "ph-crow__b"),
            ], "ph-crow"))
        else:
            blocks[-1]["elements"][1]["elements"].append(p(para, "ph-terms"))

    # Plain text for the phone and the date. Elementor's tel and date fields
    # carry their own format validation, and a field type that rejects what
    # somebody typed is worse here than no check at all - this form is the one
    # place on the site where a rejected submission loses a sale.
    # No form. Abigail signs with the buyer in person at pickup, so the page's
    # job is to let somebody read the agreement before they get there.
    blocks.append(row([
        con([p("Signing", "ph-cnum"),
             h("How this gets signed", "ph-ctitle", tag="h3")], "ph-crow__n"),
        con([p("There is nothing to sign here. Read the agreement, ask us about "
               "anything you are unsure of, and we will sign a copy together "
               "when you come to collect your puppy.", "ph-terms"),
             p("Questions first? Call 207-703-8043 or email "
               "pinehillgermanshepherds@gmail.com.", "ph-note")],
            "ph-crow__b"),
    ], "ph-crow ph-sign"))

    d.append(sec([con(blocks, "ph-doc")], "terms", tone="white"))
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
.ph-doc{max-width:1040px!important;margin-inline:auto!important;padding:0!important;gap:0!important;
 align-items:flex-start!important}
/* Title, clauses and signature share the one column, so the page reads as a
   single document rather than three stacked bands. */
/* The masthead is centred like the head of a printed agreement; the clauses
   below stay on their left rail, which is what makes them scannable. */
.ph-mast{width:100%!important;max-width:none!important;align-items:center!important;
 text-align:center!important;gap:0!important;padding:0 0 clamp(26px,3vw,36px)!important;
 margin-bottom:clamp(30px,3.4vw,42px)!important;border-bottom:1px solid var(--hair)!important}
.ph-mast__co p{margin-bottom:4px!important;font-size:clamp(24px,2.4vw,30px)!important}
.ph-title .elementor-heading-title{font-size:clamp(26px,2.8vw,34px)!important;
 letter-spacing:-.015em!important;margin-bottom:12px!important}
.ph-mast__note p{font-size:14px!important;line-height:1.8!important;max-width:58ch!important;
 margin-inline:auto!important;color:var(--body)!important;padding-top:4px!important}
.ph-doc>.ph-lede p{font-size:16.5px!important;line-height:1.8!important;max-width:74ch!important;
 color:var(--espresso)!important;padding-bottom:clamp(14px,2vw,24px)!important}

@media(max-width:820px){
.ph-crow{flex-direction:column!important;gap:14px!important}
.ph-crow__n{flex:0 0 auto!important;flex-direction:row!important;align-items:baseline!important;
 gap:12px!important}
.ph-crow__b{max-width:none!important}
.ph-cnum p{font-size:19px!important}
}
.ph-sign{border-top:1px solid var(--espresso)!important;
 margin-top:clamp(18px,2.4vw,32px)!important;padding-top:clamp(34px,4vw,48px)!important}
.ph-sign .ph-cnum p{font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;
 font-weight:600!important;letter-spacing:.22em!important;text-transform:uppercase!important;
 padding-top:6px!important}
.ph-sign .ph-terms p{padding-bottom:22px!important}
.ph-sign .ph-note p{padding-top:16px!important}
/* One clause: the rail on the left, the wording on the right. */
.ph-crow{display:flex!important;flex-direction:row!important;align-items:flex-start!important;
 gap:clamp(28px,4.5vw,72px)!important;width:100%!important;max-width:none!important;
 padding:clamp(28px,3.2vw,40px) 0!important;border-top:1px solid var(--hair)!important}
.ph-crow__n{flex:0 0 clamp(160px,20%,230px)!important;width:auto!important;max-width:none!important;
 gap:8px!important;padding:0!important;align-items:flex-start!important}
.ph-crow__b{flex:1 1 0!important;min-width:0!important;width:auto!important;max-width:680px!important;
 gap:0!important;padding:0!important;align-items:flex-start!important}
.ph-cnum p{font-family:'Cormorant Garamond',Georgia,serif!important;font-size:24px!important;
 line-height:1!important;color:var(--brass)!important;letter-spacing:.04em!important}
.ph-ctitle .elementor-heading-title{font-size:20px!important;line-height:1.25!important;
 letter-spacing:-.005em!important}
.ph-terms p{font-size:15px!important;line-height:1.85!important;padding-bottom:14px!important}
.ph-terms:last-child p{padding-bottom:0!important}
/* Gravity Forms, dressed to match the rest of the site. Targets Gravity's own
   markup rather than Elementor's, because the form is a Gravity form. */
.ph-gf .gform_wrapper .gfield_label,.ph-gf .gform_wrapper legend.gfield_label{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;
 font-weight:600!important;letter-spacing:.14em!important;text-transform:uppercase!important;
 color:var(--brass)!important;margin-bottom:8px!important}
.ph-gf .gform_wrapper .gform_fields{row-gap:22px!important}
.ph-gf .gform_wrapper input[type=text],.ph-gf .gform_wrapper input[type=email],
.ph-gf .gform_wrapper input[type=tel],.ph-gf .gform_wrapper input[type=url],
.ph-gf .gform_wrapper textarea,.ph-gf .gform_wrapper select{
 border:1px solid var(--hair)!important;border-radius:0!important;background:#FFFFFF!important;
 padding:13px 14px!important;font-family:'Montserrat',system-ui,sans-serif!important;
 font-size:14px!important;color:var(--espresso)!important;box-shadow:none!important}
.ph-gf .gform_wrapper input:focus,.ph-gf .gform_wrapper textarea:focus,
.ph-gf .gform_wrapper select:focus{outline:2px solid var(--brass)!important;
 outline-offset:2px!important;border-color:var(--brass)!important}
.ph-gf .gform_wrapper .gfield--type-consent .gfield_consent_label,
.ph-gf .gform_wrapper .ginput_container_consent label{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:13.5px!important;
 font-weight:400!important;letter-spacing:0!important;text-transform:none!important;
 color:var(--body)!important;line-height:1.7!important}
.ph-gf .gform_wrapper .gfield_required{color:var(--brass)!important}
.ph-gf .gform_wrapper .gform_footer{margin-top:28px!important;padding:0!important}
/* The submit button. Written wide and with body in front of it because the
   styler widget paints its own blue over anything weaker, and Gravity renders
   the button as an input on some versions and a button element on others. */
body .ph-gf .gform_footer input[type=submit],
body .ph-gf .gform_footer button[type=submit],
body .ph-gf .gform_footer .gform_button,
body .ph-gf input.gform_button,
body .ph-gf button.gform_button,
body .ph-gf .gform_wrapper .gform_footer input,
body .ph-gf .gform_wrapper .gform_footer button{
 background:var(--sage)!important;background-color:var(--sage)!important;
 background-image:none!important;color:var(--ivory)!important;
 border:0!important;border-color:var(--sage)!important;
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;
 font-weight:500!important;letter-spacing:.2em!important;text-transform:uppercase!important;
 border-radius:0!important;padding:17px 34px!important;width:auto!important;
 box-shadow:none!important;text-shadow:none!important;cursor:pointer!important;
 transition:transform .3s cubic-bezier(.22,.9,.32,1),background-color .25s ease!important}
body .ph-gf .gform_footer input[type=submit]:hover,
body .ph-gf .gform_footer button[type=submit]:hover,
body .ph-gf .gform_footer .gform_button:hover{
 background:var(--sage-deep)!important;background-color:var(--sage-deep)!important;
 color:var(--ivory)!important;transform:translateY(-2px)}
body .ph-gf .gform_footer input[type=submit]:focus-visible,
body .ph-gf .gform_footer button[type=submit]:focus-visible,
body .ph-gf .gform_footer .gform_button:focus-visible{
 outline:2px solid var(--brass)!important;outline-offset:3px!important}
.ph-gf .gform_wrapper .gform_confirmation_message{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:15px!important;
 color:var(--espresso)!important;line-height:1.8!important}
.ph-gf .gform_wrapper .gform_validation_errors{border-radius:0!important}
.elementor-element-litherow10 img{height:auto!important;object-fit:contain!important}
"""

# ============================================================= OUR SHEPHERDS
# Everything on this page is Abigail's own: registration numbers, health
# results and the documents behind them. Nothing here is written from
# imagination - if a fact is not in hand it is left as a visible blank.
def shepherds():
    start("shd")

    d = [hero("Our Shepherds", "the dogs behind every litter",
              "pair", ypos=48, tall=False)]

    d.append(sec([head(None,
                       "Two dogs, fully tested",
                       "Every puppy we place comes from these two. Their "
                       "registrations, hips, elbows, heart and eyes are all "
                       "on record, and the paperwork is linked below so you "
                       "can read it yourself rather than take our word for it.")],
                 "intro", tone="white", tight=True))

    # ---- Freda
    freda_facts = [
        ("Call name", "Freda"),
        ("Registered", FREDA["name"]),
        ("Date of birth", FREDA["dob"]),
        ("AKC number", FREDA["akc"]),
        ("Hips", link("PennHIP results", FREDA["hips"])),
        ("Elbows", link("OFA elbow report", FREDA["elbows"])),
        ("Heart", link("Cardiac result", FREDA["heart"])),
        ("Eyes", link("OFA CAER result", FREDA["eyes"])),
        ("Pedigree", link("Five-generation pedigree", FREDA["pedigree"])),
    ]
    d.append(sec([split(
        img("freda", "ph-frame"),
        col([p("Our foundation female", "ph-role"),
             h("Freda von Stephanitz"),
             rule(False),
             p("Freda is the dam behind our litters and the reason the "
               "kennel exists. She is health-tested in full, and every "
               "result below is a document you can open.", "ph-lede"),
             dl(freda_facts)]),
    )], "freda", tone="linen"))

    # ---- Rangeley
    rang_facts = [
        ("Call name", RANGELEY["call"]),
        ("Registered", RANGELEY["name"]),
        ("AKC number", RANGELEY["akc"]),
        ("Hips and elbows", "OFA Good / Normal"),
        ("Heart", "OFA Advanced Echocardiogram, Normal"),
        ("Eyes", "OFA CAER, Normal"),
        ("Genetics", "Embark, clear"),
    ]
    d.append(sec([split(
        col([p("The sire of our current litter", "ph-role"),
             h("Ledger Bei Mackenzie"),
             rule(False),
             p("Rangeley is the sire behind Litter A. He is fully health "
               "tested and genetically clear.", "ph-lede"),
             dl(rang_facts)]),
        img("rangeley1", "ph-frame"),
    )], "sire", tone="white"))

    d.append(sec([head(None, "Rangeley at work", None),
                  quad([img(k, "ph-frame ph-frame--sq")
                        for k in ("rangeley2", "rangeley3", "rangeley5",
                                  "rangeley6")])],
                 "gallery", tone="linen"))

    d.append(cta("Puppies from these two",
                 "Litter A is on the ground. Reservations are open and the "
                 "waiting list is short.",
                 "See Available Litters", "/litters-new/", image_key="band2"))
    return d



PAGES = {"puppies": puppies, "litters": litters, "contract": contract,
         "shepherds": shepherds}

if __name__ == "__main__":
    name, mode = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "data")
    data = PAGES[name]()
    j, c = emit(data, EXTRA)
    if mode == "data":
        sys.stdout.write(j)
    elif mode == "wire":
        # The MCP meta write runs stripslashes on the value, so a lone
        # backslash never survives the trip: "Male\\nFemale" arrives as
        # "MalenFemale" and the select renders one nonsense option. Doubling
        # every backslash first means stripslashes hands WordPress exactly the
        # JSON this file generated. \uXXXX is decoded in transit instead, so it
        # arrives as the real character and needs no doubling - only the
        # backslash matters.
        sys.stdout.write(j.replace("\\", "\\\\"))
    elif mode == "css":
        sys.stdout.write(c)
    elif mode == "index":
        import json
        sys.stdout.write(json.dumps(INDEX, indent=1))
