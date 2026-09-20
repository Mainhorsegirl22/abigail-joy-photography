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
from phkit import (start, section, con, row, w, h, p, ul, dl, btn, img, rule, form, opener,
                   bighero, intro, vals, trivia, ph_img, splittop, quiettop,
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
    start("shp")
    d = [quiettop("Meet Our Shepherds", "our family",
                  "Two dogs. Every health result is on file, and the paperwork "
                  "is linked so you can read it yourself.", tone="sand")]

    # Each dog gets a full row, the photograph alternating side to side.
    d.append(sec([row([
        img("freda", "ph-frame2"),
        con([p("Dam \u00b7 dark sable \u00b7 search and rescue", "ph-dogname"),
             h(FREDA["name"], tag="h2"), rule(False),
             p("Freda is our only breeding female, and a family member first. "
               "Everything we plan is built around her, which is why we raise "
               "one litter at a time."),
             dl([("Date of birth", FREDA["dob"]),
                 ("AKC", FREDA["akc"]),
                 ("Hips", link("PennHIP \u2014 see result", FREDA["hips"])),
                 ("Elbows", link("OFA Normal \u2014 see result", FREDA["elbows"])),
                 ("Heart", link("OFA Normal \u2014 see result", FREDA["heart"])),
                 ("Eyes", link("OFA Normal \u2014 see result", FREDA["eyes"])),
                 ("Genetics", "Clear")]),
             btn("Meet Freda", "/freda-new/", "ph-pillbtn")],
            "ph-dog"),
    ], "ph-asplit")], "freda", tone="white"))

    d.append(sec([row([
        con([p(f"Sire \u00b7 called {RANGELEY['call']}", "ph-dogname"),
             h(RANGELEY["name"], tag="h2"), rule(False),
             p("Rangeley is the sire of our current litter. His results are "
               "searchable on the OFA site under his registration number."),
             dl([("AKC", RANGELEY["akc"]),
                 ("Hips", "OFA Good"),
                 ("Elbows", "OFA Normal"),
                 ("Heart", "OFA Advanced Echocardiogram, Normal"),
                 ("Eyes", "OFA CAER Normal"),
                 ("Genetics", "Embark, clear")]),
             btn("Meet Rangeley", "/rangeley-new/", "ph-pillbtn")],
            "ph-dog"),
        img("rangeley1", "ph-frame2"),
    ], "ph-asplit")], "rangeley", tone="linen"))

    d.append(vals("What We Test For, Every Time",
                  "On both parents, before any breeding\u2026",
                  [("<svg viewBox='0 0 48 48'><path d='M24 6v12'/><path d='M24 18c-7 0-12 5-12 12v12'/><path d='M24 18c7 0 12 5 12 12v12'/><circle cx='16' cy='30' r='4'/><circle cx='32' cy='30' r='4'/></svg>", "Hips and Elbows"), ("<svg viewBox='0 0 48 48'><path d='M24 40s-14-8-14-18a7.5 7.5 0 0114-4 7.5 7.5 0 0114 4c0 10-14 18-14 18z'/><path d='M12 22h6l3-5 4 10 3-5h8'/></svg>", "Heart"),
                   ("<svg viewBox='0 0 48 48'><path d='M4 24s8-11 20-11 20 11 20 11-8 11-20 11S4 24 4 24z'/><circle cx='24' cy='24' r='6'/></svg>", "Eyes"), ("<svg viewBox='0 0 48 48'><path d='M16 6c0 12 16 12 16 24s-16 12-16 12'/><path d='M32 6c0 12-16 12-16 24s16 12 16 12'/><path d='M18 14h12M16 22h16M16 30h16M18 38h12'/></svg>", "Genetic Panel")]))

    d.append(cta("Puppies From These Two",
                 "Litter A is on the ground. The waiting list is short.",
                 "See Available Litters", "/litters-new/", image_key="band2"))
    return d

# =============================================================== EACH DOG
# One page per dog, reached by clicking through from Meet Our Shepherds.
# Registered name, a write-up, the full results, and that dog's own photos.
def _dog(tag, call, kicker, lede, story, facts, photos, hero_key,
         reverse=False):
    start(tag)
    pic = img(hero_key, "ph-frame2")
    txt = con([p(kicker, "ph-dogname"), h(call, tag="h1"), rule(False),
               p(lede, "ph-lede")], "ph-dog")
    # the photo falls on the opposite side for the second dog, so the two
    # pages do not read as the same page twice
    d = [sec([row([txt, pic] if reverse else [pic, txt], "ph-asplit")],
             "top", tone="sand")]

    d.append(sec([con([p(s) for s in story], "ph-mid")],
                 "story", tone="white", tight=True))

    d.append(sec([head("on file", "Health and Registration",
                       "Every result below is a real document. Click any of "
                       "them."),
                  con([dl(facts)], "ph-narrow")], "health", tone="linen"))

    d.append(sec([head(None, f"{call} in Pictures"),
                  row([img(k, "ph-gcell") for k in photos], "ph-grid")],
                 "gal", tone="white"))

    d.append(cta("Puppies From Our Programme",
                 "Reservations for the next litter are open.",
                 "Reserve a Puppy", "/reserve-a-puppy-new/", image_key="band2"))
    return d


def freda():
    return _dog(
        "fre", "Freda", "Dam \u00b7 dark sable \u00b7 search and rescue",
        FREDA["name"],
        ["Freda is our main breeding female here at Pine Hill German "
         "Shepherds, and a beloved family member. There are truly no words to "
         "express what a special dog Freda is to me. She has been a huge part "
         "of my life, and I am very thankful for her.",
         "Because she is our only breeding female, we can plan every litter "
         "around her and give each one the same attention. She is trained in "
         "scent detection and search and rescue work, and she passes that "
         "drive and that steadiness on to her puppies.",
         "Her full health testing is below, with every certificate linked so "
         "you can read the results yourself rather than take our word for it."],
        [("Registered name", FREDA["name"]),
         ("Call name", "Freda"),
         ("Date of birth", FREDA["dob"]),
         ("AKC registration", FREDA["akc"]),
         ("Hips", link("PennHIP \u2014 see result", FREDA["hips"])),
         ("Elbows", link("OFA Normal \u2014 see result", FREDA["elbows"])),
         ("Heart", link("OFA Normal \u2014 see result", FREDA["heart"])),
         ("Eyes", link("OFA Normal \u2014 see result", FREDA["eyes"])),
         ("Genetic panel", "Clear"),
         ("Pedigree", link("Read her pedigree", FREDA["pedigree"]))],
        ["freda", "portrait", "sunlit", "pair", "breeders", "farm"],
        "freda")


def rangeley():
    return _dog(
        "ran", "Rangeley", f"Sire \u00b7 {RANGELEY['akc']}",
        RANGELEY["name"],
        ["Rangeley is the sire of our current litter. He is a working-line "
         "male with full OFA health testing behind him \u2014 hips, elbows, "
         "heart and eyes \u2014 and an Embark genetic panel that came back clear.",
         "More about his temperament and his work: " +
         fill("Abigail to write") + ".",
         "His results are on file with the OFA and are searchable under his "
         "registration number."],
        [("Registered name", RANGELEY["name"]),
         ("Call name", RANGELEY["call"]),
         ("AKC registration", RANGELEY["akc"]),
         ("Hips", "OFA Good"),
         ("Elbows", "OFA Normal"),
         ("Heart", "OFA Advanced Echocardiogram, Normal"),
         ("Eyes", "OFA CAER Normal"),
         ("Genetic panel", "Embark, clear")],
        ["rangeley1", "rangeley2", "rangeley3", "rangeley4",
         "rangeley5", "rangeley6", "rangeley7", "working", "montie"],
        "rangeley1", reverse=True)


# ==================================================================== ABOUT
# Abigail's own copy from the live About page, restructured rather than
# rewritten. Two typos in the source are corrected: "exited" -> "excited" and
# the heading "Scent Dedectino and SAR Taining".
def about():
    start("abt")
    d = [bighero("Raised In Our Home,<br>Not In A <em>Kennel</em>.",
                 "welcome to Pine Hill", slot="Hero+photo")]

    d.append(intro(
        "Small Family Breeder of Working Line German Shepherds",
        "Based in Garland, Maine \u2014 raised for work, for sport, and for "
        "family life.",
        "We are a small family business raising working-line German Shepherds "
        "on 40 acres of rural countryside in the backwoods of New England. We "
        "specialise in dogs known for their personalities, working drive, "
        "scent detection ability and balanced temperaments, and our focus is "
        "early puppy socialisation, development and training."))

    d.append(sec([row([
        ph_img("Portrait+photo", 900, 1125),
        con([p("With only one breeding female \u2014 Freda, our beloved family "
               "member \u2014 we can plan each litter carefully and spend "
               "countless hours observing and working with the puppies. That "
               "lets us shape their early training and socialisation using "
               "tested, proven methods."),
             p("Raised inside our home and surrounded by our family, our "
               "puppies get plenty of love and care from day one. Every puppy "
               "has its own personality, just as every person does, and our "
               "goal is to match each one to the family that suits it best."),
             btn("Meet Our Shepherds", "/our-shepherds-new/", "ph-pillbtn")],
            "ph-acol"),
    ], "ph-asplit")], "story", tone="white", tight=True))

    d.append(vals("When It Comes To Our Dogs And Our Families",
                  "We\u2019re committed to\u2026",
                  [("<svg viewBox='0 0 48 48'><path d='M24 5l14 5v12c0 10-6 17-14 21-8-4-14-11-14-21V10z'/><path d='M17 23l5 5 10-11'/></svg>", "Health Testing"),
                   ("<svg viewBox='0 0 48 48'><path d='M24 41s-14-8.5-14-18.5A7.6 7.6 0 0124 18a7.6 7.6 0 0114 4.5c0 10-14 18.5-14 18.5z'/><ellipse cx='24' cy='28' rx='3.8' ry='3.1'/><ellipse cx='18.6' cy='23.4' rx='1.7' ry='2.2'/><ellipse cx='24' cy='21.6' rx='1.7' ry='2.2'/><ellipse cx='29.4' cy='23.4' rx='1.7' ry='2.2'/></svg>", "Puppy Culture"),
                   ("<svg viewBox='0 0 48 48'><path d='M13 41V27c0-4 1-7 3-9.5L17 6l6.5 9.5L26 13l5 8.5c2 1.5 3.5 3 4.5 4.5L43 29l-1 2.5-6-1.5'/><path d='M31 30c0 5-3 9-8 11'/><circle cx='25' cy='21' r='1.1'/></svg>", "Responsible Breeding"),
                   ("<svg viewBox='0 0 48 48'><path d='M6 12h21v15H17l-8 6v-6H6z'/><path d='M25 22h17v13h-6l-6 5v-5h-5z'/></svg>", "Lifetime Support")]))

    d.append(trivia("Rapid fire", "Pine Hill Edition", [
        ("01", "We have exactly one breeding female. Freda is a family member "
               "first and a foundation dam second."),
        ("02", "Hiking, swimming, horseback riding \u2014 our shepherds come "
               "along for all of it."),
        ("03", "Every puppy is raised inside our home, underfoot, from the day "
               "it is born."),
    ]))
    return d


# =========================================================== RESERVE A PUPPY
# Top: opener() - title on clean ground above a wide photograph. Rhythm:
# intro, reversed split, numbered process, form. Deliberately not About's.
def reserve():
    start("res")
    d = [opener("Reserve a Puppy", "your next companion", "portrait",
                "Carefully planned litters, bred for personal protection, "
                "detection work, search and rescue, and active family life.")]

    d.append(sec([con([
        p("Each of our puppies is precious to us, and we dedicate many hours "
          "to early socialisation, early puppy development and Early Scent "
          "Introduction. Because their welfare matters to us, we guide every "
          "potential buyer through a thorough application process, to be sure "
          "one of our puppies is genuinely a good fit. We will do our best to "
          "match you with the right puppy."),
    ], "ph-mid")], "intro", tone="white", tight=True))

    # photo on the RIGHT here, the mirror of About's split
    d.append(sec([row([
        con([h("Before You Apply", tag="h2"), rule(False),
             p("Buying a working-line German Shepherd is a significant "
               "commitment. We strongly encourage you to research the breed "
               "thoroughly before bringing a puppy home."),
             p("These are not typical German Shepherds. They are bred for "
               "work \u2014 protection, tracking, detection. They are highly "
               "energetic and are not suited to a sedentary household."),
             p("Only buyers confident they have the time, the resources and "
               "the willingness to train and properly care for a working-line "
               "puppy should apply. Our " +
               here("sales contract", "/sales-contract-new/") +
               " is published in full, so you can read every term before you "
               "commit to anything.")], "ph-acol"),
        img("scholars", "ph-frame2"),
    ], "ph-asplit")], "consider", tone="linen"))

    d.append(sec([head("the process", "How a Reservation Works"), steps([
        ("01", "Apply", "Fill in the application below. It tells us about "
                        "your home, your experience and what you want in a dog."),
        ("02", "We talk", "We read every application and reply. If a puppy "
                          "from us is not right for your situation, we say so."),
        ("03", "Deposit", "A deposit holds your place. Reservations are taken "
                          "in the order deposits arrive, and the waiting list "
                          "is kept by gender."),
        ("04", "Matching", "Puppies are matched to families at around six "
                           "weeks, on temperament rather than who asked first."),
        ("05", "Home", "The balance is due at pickup. Collect from us in "
                       "Garland, or ask about delivery."),
    ])], "process", tone="white"))

    d.append(sec([head("apply", "Puppy Application",
                       "Take your time with this. The more we know, the "
                       "better we can match you."),
                  con([gform(5)], "ph-formwrap")], "apply", tone="linen"))

    d.append(cta("Questions First?",
                 "Call 207-703-8043. We would rather answer a question now "
                 "than have a puppy go to the wrong home.",
                 "Contact Us", "/contact-new/", image_key="band2"))
    return d


# ================================================================== CONTACT
# Top: quiettop() - no photograph at all. A short, practical page.
def contact():
    start("con2")
    d = [quiettop("Get in Touch", "we would love to hear from you",
                  "Questions about a puppy, a litter, or the breed \u2014 ask.",
                  tone="linen")]

    d.append(sec([row([
        con([dl([("Phone", "207-703-8043"),
                 ("Email", "pinehillgermanshepherds@gmail.com"),
                 ("Where", "Garland, Penobscot County, Maine"),
                 ("From Bangor", "About one hour"),
                 ("From Portland", "About two hours")]),
             p("Puppies are collected from our home. If you cannot make the "
               "trip, ask about delivery \u2014 we are happy to work with you.",
               "ph-measure")], "ph-acol"),
        con([gform(1)], "ph-formwrap"),
    ], "ph-asplit")], "reach", tone="white"))

    d.append(cta("Ready to Apply?",
                 "If you have read the contract and a working-line Shepherd "
                 "suits your home, start the application.",
                 "Reserve a Puppy", "/reserve-a-puppy-new/", image_key="band2"))
    return d


# ================================================================== GALLERY
# Top: quiettop() on sand, then the page is almost entirely photographs.
def gallery():
    start("gal")
    d = [quiettop("Gallery", "our shepherds", tone="sand")]

    # One gallery, not three sections. Every photograph in a single grid.
    d.append(sec([row([img(k, "ph-gcell") for k in (
        "freda", "rangeley1", "portrait", "puppies", "scholars", "litter_band",
        "breeders", "rangeley2", "rangeley3", "rangeley5", "working", "farm",
        "pair", "sunlit", "rangeley6")], "ph-grid")], "all", tone="white"))

    d.append(cta("Interested in a Puppy?",
                 "Reservations for our next litter are open.",
                 "Reserve a Puppy", "/reserve-a-puppy-new/", image_key="band2"))
    return d

# ===================================================================== NEWS
# Top: quiettop() on linen. The quietest page on the site, deliberately.
def news():
    start("nws")
    d = [quiettop("News", "from the kennel",
                  "Litter announcements, health testing results, training "
                  "updates and the occasional photograph of a very muddy dog.",
                  tone="linen")]

    d.append(sec([con([
        p("Post feed goes here \u2014 " + fill("wire to the blog") + "."),
        p("The most reliable way to hear about a litter first is the waiting "
          "list. People on it hear before an announcement goes anywhere else."),
        btn("Join the Waiting List", "/reserve-a-puppy-new/"),
    ], "ph-mid")], "feed", tone="white"))

    d.append(cta("Want to Hear First?",
                 "The waiting list is short and it moves.",
                 "Join the Waiting List", "/reserve-a-puppy-new/",
                 image_key="litter_band"))
    return d


# ============================================================= PUPPY CULTURE
# Top: splittop() - photograph beside the title, a third silhouette again.
def puppy_culture():
    start("pc")
    d = [splittop("Puppy Culture", "the first nine weeks",
                  "As breeders we have an almost magical ability to influence "
                  "what happens later in our puppies\u2019 lives. We take that "
                  "seriously.", slot="Puppies+photo")]

    d.append(sec([con([
        p("Our puppies are raised using Puppy Culture, ESI (Early Scent "
          "Introduction) and early socialisation techniques."),
        p("Every puppy has a unique personality, and we have the opportunity "
          "to be part of the first nine weeks of their lives \u2014 shaping and "
          "nurturing that potential before they ever come home to you."),
        p(link("Read more about Puppy Culture",
               "https://shoppuppyculture.com/pages/about-puppy-culture")),
    ], "ph-mid")], "culture", tone="white", tight=True))

    d.append(sec([head("k9 scholars", "The Five-Week Programme",
                       "Given a structured environment suited to their rapidly "
                       "developing brains, puppies learn remarkably fast. Over "
                       "five weeks they learn advanced manners and meet new "
                       "situations."),
                  con([ul([
                      "Advanced manners \u2014 sit, stay, come, leash training",
                      "Introduction to car rides",
                      "Crate training",
                      "Manding \u2014 the automatic sit",
                      "Food manners",
                      "Advanced socialisation",
                      "Daily handling, and a great deal of love",
                      "Problem-solving exercises",
                      "Scent detection exercises",
                      "Confidence-building exercises",
                      "Being well behaved around children and seniors",
                      "Manners in public",
                  ])], "ph-narrow")], "scholars", tone="linen"))

    d.append(trivia("What it means", "Why We Bother", [
        ("01", "A puppy that has met noise, surfaces, crates and strangers "
               "before nine weeks meets the rest of life the same way."),
        ("02", "Early Scent Introduction is a few seconds a day. The dogs it "
               "produces work with their noses for a lifetime."),
        ("03", "We would rather do the hard weeks here than hand you a puppy "
               "that has to unlearn something."),
    ]))
    return d


PAGES = {"puppies": puppies, "litters": litters, "contract": contract,
         "shepherds": shepherds, "about": about, "reserve": reserve,
         "contact": contact, "gallery": gallery, "news": news,
         "puppyculture": puppy_culture, "freda": freda,
         "rangeley": rangeley}

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
