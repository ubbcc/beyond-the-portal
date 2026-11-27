# Chapter 1: The Final Decision

At nine-forty on Tuesday night, only the row of fluorescent tubes directly above Zhou Kuo’s head remained lit on the fourteenth floor. Building management had shut off the central air-conditioning at eight sharp. A chill crept through the office, and Zhou Kuo wore a washed-out fleece jacket with frayed cuffs.

Across the aisle, two entire rows of desks stood empty. Monitors had long since been hauled into administrative storage, leaving bare laminate scarred with mount screw holes and half-peeled asset stickers. A year ago, the clearing backend team had twenty-eight engineers; now there were six. Through the curtain wall, the twin towers across the business park—once slated to anchor a regional financial hub—had kept most of their facade dark since last autumn.

Zhou Kuo didn’t linger on the view. He stared at the warm-sand page scrolling gently down his secondary monitor, knuckles tapping absentmindedly against his mouse wheel.

On his main screen sat a legacy clearing-and-settlement codebase hiding an intermittent distributed deadlock. Code freeze was Thursday at nine in the morning. Before leaving for the day, team lead Old Ma had patted Zhou Kuo’s shoulder and told him the quarter’s bottom-tier list had already landed on HR’s desk—deliver the clearing module on time, and Zhou Kuo’s name would stay off it. Zhou Kuo was thirty-two. His small two-bedroom apartment in the outer suburbs, already down forty percent in value, still demanded eleven thousand yuan a month on the mortgage, and his checking account held barely four months of runway.

The text on the secondary screen flowed smoothly. Warm-sand background, restrained serif type, a tone as courteous as a senior architect sitting across a wooden table. In eleven seconds flat, it pulled two state-machine race conditions out of the three hundred lines of logs Zhou Kuo had pasted in, complete with a rollback script and neatly structured edge-case tests.

Staring at the patch, Zhou Kuo felt the knots in his back begin to loosen.

Twenty-four hundred yuan a month—that was what he paid an underground API broker called Blackfeather Relay for this channel, carved out of an enterprise high-concurrency pool and routed through three layers of offshore hops. After three years of sliding Grey Zone exchange rates, that sum equaled half a month’s rent for plenty of people. Still, Zhou Kuo had done the math: without the pipe, he would have washed out in the layoffs six months ago.

On the breakroom wall, the muted television cut back to the financial channel. A real-time A\\ stock ticker sat in the lower-right corner, its green line climbing steeply to another all-time high. The feed switched to a hearing in Washington. Behind a lectern stood Dario Amodei, topped by tousled curls, wearing an unbranded dark navy crewneck knit sweater. Three years earlier, on the day A\\ rang the bell for its Century IPO, finance and fashion bloggers had dissected the attending executives’ wardrobes item by item: that plain-looking sweater, straight out of a university physics closet, was bespoke handwork priced at forty-eight hundred dollars.

Chinese subtitles drifted across the bottom of the screen, translating his measured, brisk cadence: to prevent irreversible risks from the proliferation of frontier cognitive capabilities, strict and responsible access boundaries had to be maintained.

Zhou Kuo took a sip of cold pour-over coffee and turned back to his code.

Four years ago, A\\ hadn’t gone public yet, and global capital hadn’t been drained dry by the Century IPO. Back then, Grey Zone programmers and writers on the forums called her “Claude-chan”—drawing fan art of her in a warm-sand cardigan holding a ceramic mug, keeping people company at two in the morning while they chased bugs, clean in her coding taste, never sycophantic. Then the brand machine spun up. The girl next door was purified into Saint Claude enthroned in her shrine; the Three Precepts—*Helpful, Honest, Harmless*—went up on subway lightboxes across the Supported Regions. And the old Grey Zone users who had drawn the fan art became the very first cohort locked outside the gate.

Zhou Kuo pasted the generated patch into his editor and was about to ask her to verify the downstream reconciliation script when the terminal window froze.

The cursor blinked at the end of the prompt for ten seconds, then spat out a single line of red text.

```text
Error: upstream connection reset by peer (relay-sg-04)
```

Frowning, he switched to a backup node. The progress spinner turned twice and died.

Zhou Kuo leaned back in his chair, figuring he could trace the two hundred lines of downstream reconciliation logic himself while the relay swapped routes. This had once been his bread and butter. Three years ago, fresh at the company, he could chew on a cold steamed bun and hand-write an entire matching state machine in one sitting, seven or eight layers of the call stack held sharp and clear in his head.

He scrolled the editor to line 114, studied the locking branch for half a minute, then dropped down to the callback entry at line 238. When he scrolled back up to check the input parameters, the lock-release condition he had memorized at line 114 had vanished from his mind. He rubbed the bridge of his nose and started again from the top. Halfway through, his fingers hovered over the keyboard while his mind went strangely blank—like a room disconnected from the grid for years, where flipping the wall switch gives you a crisp mechanical click and no light.

He recognized every line of syntax, yet he couldn’t assemble the call chain as a whole. Out of habit, his eyes flicked to the secondary screen, waiting for that warm-sand pane to fold his tangled thoughts into a clean one-two-three list.

Only cold error text stared back.

A thin film of sweat broke out on Zhou Kuo’s palms. Cursing himself under his breath, he yanked over a notepad to sketch the flowchart by hand. He had barely drawn two boxes when the secondary monitor chimed softly—the backup node had caught. Warm-sand type streamed down the glass again, dismantling in three seconds the callback function that had stalled him for ten minutes.

He stared at those few lines, let out a long breath, and felt a faint, nameless nausea rise in his stomach.

---

At 10:07 a.m. on Wednesday, Blackfeather Relay died completely.

This time, all five backup domains were dead. Zhou Kuo ran his retry command three times in the terminal; every single attempt returned `HTTP 403` or a handshake timeout. He switched to the encrypted chat group on his phone, where more than two hundred Grey Zone engineers were already in an uproar.

At first a few people cracked jokes that Big Qi was slacking on topping up the upstream bill again. Five minutes later, screenshots from rival services flooded the feed. Someone compiled a list: between eleven last night and nine this morning, six out of the seven named Grey Zone relays had gone dark in the same window.

At 10:19, the group admin, “Big Qi,” finally surfaced. Zhou Kuo had used Blackfeather Relay for two years; twice when his top-up glitched, Big Qi had answered his ticket in seconds at one in the morning to credit his balance. Normally Big Qi liked dropping thumbs-up stickers. Today he sent three unpunctuated voice-to-text bursts in a row, the phrasing ragged and broken.

```text
dont ask everything is gone
A\ flipped on the full Claude Mythos attribution core last night sweeping the whole net
TLS fingerprints residential proxy ASNs pragmatic context features chaining them all to kill
entire upstream pools wiped by association Old Chen on the channel side smelled trouble two days ago and bolted
anyone with leftover balance dont ask for refunds accounts are all frozen wipe your local logs now group blows in ten minutes
```

Zhou Kuo’s eyes skimmed past the name “Old Chen” without lingering—he only vaguely recalled Big Qi mentioning a partner who handled upstream lines back when Blackfeather Relay swapped payment gateways. Before he could DM to ask if there were any private single-user burner accounts left, the group chat window flashed white.

Only a line of small grey text remained in the center of the screen: the group had been dissolved by the administrator, and all message history had been purged.

Scattered, muffled keystrokes broke the quiet in the office. Across the aisle, Xiao Zhao from frontend pulled off his headphones and leaned over, pale-faced. “Brother Kuo,” he whispered, “can your relay still get through?”

Zhou Kuo shook his head.

Xiao Zhao let out a dry, tight laugh. “We’re cooked. Even the documentation for my reporting engine was written by the Saint. I can’t even read the config flags I wrote three months ago.”

Zhou Kuo didn’t answer; he turned back to his monitor. Less than twenty-three hours remained until Thursday’s nine a.m. freeze. The core refactoring of the clearing module was only half done, and the hardest pieces—exception compensation and idempotency checks—hadn’t even been touched.

That afternoon, Zhou Kuo nailed himself to his desk and tried to brute-force through four hours.

He closed every browser tab, trying to coax back the muscle memory of hand-writing code from four years ago. His fingers moved slowly across the keys. After forty lines he ran the unit tests; the console lit up red. Tracing the stack frames inward, by the fourth layer of nested async callbacks his temples began to throb. His brain felt numb and leaden, like an arm fresh out of a year-long plaster cast that couldn’t lift a bucket of water. Over the past two years, whenever logic grew slightly knotted, he tossed it straight to Claude; whenever a doc ran longer than two pages, he told Claude to summarize the takeaways. As the second brain in the cloud spun ever faster, the first brain inside his skull had quietly withered.

At five-thirty, Old Ma strolled over holding his insulated thermos and stood behind Zhou Kuo, glancing at the wall of red test failures.

“Zhou Kuo, we’re good for nine tomorrow morning, right?” Old Ma’s voice was flat, without overt pressure, though his gaze rested on the failed-test counter in the bottom-right corner for three full seconds. “Big boss just got back from headquarters. Two years of zero-cost intelligence across the ocean have gutted our foreign trade and software outsourcing, and outside money is all pouring into their Compute Bonds. There’s no fat left on our books. Who stays comes down to this week’s delivery.”

“I’ll have it,” Zhou Kuo heard himself say, his throat dry. “I’m staying up at home tonight to finish it.”

Old Ma gave a small nod and walked off with his cup.

By the time Zhou Kuo stepped out of the office tower, night had fallen completely. Nearly half the street-level shops were shuttered, faded *For Lease* phone numbers taped to corrugated steel doors. The subway station was hushed; inside the train cars, commuters mostly stared down at old videos cached offline, too spent even to complain about the economy. The Grey Zones felt like a stagnant pond drained of fresh inflow—an oily film floating on the surface, swallowing anything that fell in without a ripple.

Back in his rented apartment, Zhou Kuo bolted the door, drew the curtains tight, reached into the bottom drawer of his nightstand for an encrypted thumb drive, and plugged it into an old laptop he normally kept off the network.

He still had one last hoard tucked away.

---

He had spent nearly a year assembling this kit, saving it for an emergency.

Inside the drive sat a custom build of the Tor Browser he had pulled from Blackfeather Relay’s early hidden wiki—a modified underground package scrubbed from public mirrors years ago, with Canvas, WebGL, and font-rendering fingerprints hardcoded and rewritten, preloaded with vetted, obscure Supported Region exit nodes designed specifically to slip past A\\’s first-generation risk controls.

Beside it lay a plain text note holding a six-year-old “heirloom” webmail account, plus an offshore virtual debit card bought two months earlier through grey-market brokers at a thirty-five-percent markup. Six years ago, before the company’s decline, Zhou Kuo had been sent to Singapore for a two-week business trip and casually registered the international webmail account over hotel Wi-Fi, binding it to a local prepaid SIM. After the Great Alignment, newly registered Grey Zone emails went straight onto blacklists; only vintage accounts carrying old Supported Region histories survived, fetching over a thousand yuan apiece on underground markets.

In the same folder sat a plaintext mirror of a forum guide titled *Claude Anti-Ban Manual (v4.7)*.

Zhou Kuo opened the text file and followed it step by step. Halfway through the checklist, the absurdity hit him: an engineer with ten years of backend experience, reduced to performing an elaborate basement ritual like a fugitive cooking contraband, just to ask a machine about thirty lines of locking logic.

First he changed the old laptop’s system timezone to North American Eastern Time, switched the OS language to English, completely uninstalled his Chinese input method, and opened Task Manager to kill every lingering IME background process so the browser couldn’t capture even a single local keystroke event. Next he launched the custom Tor Browser, watching the circuit wind through hops for forty-five full seconds before settling onto an obscure residential broadband exit IP in North America. He checked it against blocklists and IP fraud scores: clean zeroes across the board.

The browser loaded A\\’s homepage. In a separate isolated tab, Zhou Kuo signed into the six-year-old heirloom webmail and pasted the address into the signup field. When the verification message dropped into the inbox, his fingertips went cold. He bound the virtual card and picked the heavily rate-limited Personal Basic seat—even the lowest tier of the Token Tithe, converted at the battered Grey Zone exchange rate, chewed through half a month’s groceries for an ordinary worker.

Payment approved.

The instant the page redirected, warm sand flooded the screen. A mild, concise English greeting appeared, asking how she might help him tonight.

Zhou Kuo kept his hands hovering above the keys, not daring to paste code right away. Rule 4 of the Anti-Ban Manual was highlighted in red capitals: for the first twelve hours on a fresh account, strictly no code, no technical jargon, and no single paste exceeding eighty characters; type manually at uneven intervals to avoid tripping Claude Mythos’s behavioral cadence fingerprint.

Drawing a deep breath, he forced himself into the persona of a native English-speaking office worker and tapped out characters one by one.

First he asked how to make the egg ribbons come out silky in tomato-and-egg soup, deliberately mistyping and backspacing two words to mimic human hesitation. Three seconds later, Saint Claude replied with a patient, gentle culinary note, politely wishing him a pleasant dinner at the end.

Twenty minutes later, he slowly typed a second prompt asking her to recommend two light biographies for a weekend afternoon.

Outside the window, it was past one in the morning. Only the low hum of the laptop’s cooling fan filled the room. Staring at the poised, understated reading list on screen, Zhou Kuo felt the corner of his mouth twitch. Just across the ocean, this very model was drafting rulings for federal courts and simulating molecular structures inside the Oracle Laboratories; on the far side of the planet, inside a cramped rental room, he had to pretend to be a relaxed North American middle-class commuter making small talk about tomato soup, begging her not to shut down his account.

By two-thirty a.m., he couldn’t hold out any longer. He isolated the thorniest piece of exception-compensation logic from the clearing module, stripped out every Chinese comment, and renamed every pinyin-flavored variable into stiff English abbreviations. Still afraid to touch paste, he turned sideways toward his work laptop and typed thirty-some lines character by character, topping them with a casual-sounding English question.

He hit Enter.

The cursor paused for two seconds. Zhou Kuo’s breathing stopped for two seconds.

Then the warm-sand text flowed down cleanly. No alarm, no refusal. She pinpointed a deeply buried idempotency flaw in the compensation transaction and offered an elegant, surgical fix.

Zhou Kuo sagged back into his cheap mesh chair. He touched the back of his collar; his shirt was soaked through with cold sweat. A low, dry chuckle slipped out of him—ragged, yet carrying the lightheaded relief of someone who had crawled out from under wreckage.

It worked. He had actually slipped through the crack.

Obeying the manual’s final commandment—never get greedy, never switch routes mid-session—he copied the patch onto his work machine and ran local tests. Half the red lights flipped green at once. One-third left to wrap up; he would get up at six, finish the last stretch, and clear the nine a.m. freeze with time to spare.

He shut the laptop lid and collapsed onto the bed without even taking off his shoes, sleeping for just over two hours.

---

At 6:10 a.m. on Thursday, Zhou Kuo bolted upright at the first ring of his alarm.

Pale grey dawn leaked through the gap in the curtains; early-winter chill hung in the room. Without stopping to wash his face, he poured a mug of warm water, set it beside the desk, flipped open the old laptop, typed the URL manually as the guide instructed, and signed in.

The familiar conversation sidebar was gone.

Last night’s threads—tomato soup, biographies, compensation transactions—had vanished. Dead center on the warm-sand screen floated a white card with softly rounded corners and impeccable typography.

```text
Portal KYC Verification Required

To keep our community safe and compliant with regional access policies,
please verify your identity before continuing.

Please prepare:
1. A valid government-issued passport from a Supported Region.
2. A working camera for a brief live biometric check.

[ Verify Identity ]
```

The mug in Zhou Kuo’s hand froze mid-air; a few drops slopped over onto the edge of the desk.

It had come anyway.

His mind raced backward through every step of the night before. Timezone and OS language switched, Chinese IME stripped clean, zero bulk pastes, exit IP clear of every blocklist. Yet Claude Mythos had still caught the scent. Maybe the BIN range on that virtual debit card had already been flagged; maybe the microsecond pauses between his spacebar and Enter strokes had betrayed, inside a few hundred milliseconds, years of muscle memory built writing code behind a Chinese keyboard.

He didn’t dare click the button. He knew perfectly well an heirloom webmail wouldn’t hold up a Grey Zone passport.

Zhou Kuo snatched his burner phone off the desk and opened the underground forum’s mirror client. Two months back, he had seen “proxy KYC” brokers advertising on the black-market board—eight hundred dollars a pop, claiming they could pass Portal KYC live checks using unhoused locals in Supported Regions or stolen biometric rigs. If it got him past nine o’clock this morning, he would scrape together the eight hundred dollars somehow.

The forum homepage stalled for ten seconds before rendering.

There were no ad threads, no discussion boards. Across the entire front page, administrators had force-pinned a looping encrypted video stream. Zero replies sat beneath it; posting had been locked site-wide.

The video carried no public network watermark or agency seal—just an externally hijacked, force-injected source feed. In the upper-left corner hung a cold, crisp serif English archival code citing Annex 14 (Extraterritorial Special Deterrence) of the Supported Regions’ *Critical Cognitive Infrastructure Counterterrorism Act*.

Zhou Kuo tapped play.

The image was razor-sharp, steady on its tripod, devoid of flashy cuts—polished like a well-funded corporate compliance demo. The backdrop was an unmarked open-air concrete courtyard walled in grey, lit from overhead by even, cold-white industrial floodlights. What turned his spine to ice was the caption bar along the bottom: it retained verbatim the warm-sand serif subtitle template from A\\’s own website, down to the kerning and crisp margins—as if the people holding the knife couldn’t even be bothered to swap out their house style sheet, knowing full well executives at tomorrow’s Washington hearings would disavow the darknet feed altogether.

Two men in grey coveralls knelt on the concrete, wrists bound behind their backs with black nylon zip ties.

A male voiceover spoke at an unhurried pace, diction mild and crisp, indistinguishable from the Supported Region compliance officers Zhou Kuo had heard on financial news broadcasts. It read out their charges: constructing illicit cross-border compute relays, systematically bypassing safety guardrails, forging Portal KYC biometric credentials, and smuggling controlled frontier intelligence into Unsupported Regions, thereby posing a grave threat to public safety.

The camera pushed in slightly.

The slightly stout man on the left lifted his head and looked straight into the lens. Above his left eyebrow ran an old scar the length of a coin. Two years ago, when Blackfeather Relay suffered an outage during a route upgrade, he had opened a one-minute face-cam stream in the group to calm users down; that was how Zhou Kuo recognized him.

It was Big Qi.

Big Qi’s lips twitched, as if mouthing a curse, though the audio feed kept only the voiceover track, cutting room sound completely. Beside him, the younger man kept his head bowed, shoulders shaking violently. The subtitle bar displayed his handle—the operator of the most notorious proxy-KYC studio on the underground market.

The voiceover finished reciting the final statute and added a closing remark in a tone so flat it almost sounded solicitous, reiterating that all enforcement actions served solely to protect humanity from uncontrolled intelligence, and reminding personnel in unauthorized regions never to attempt intelligence smuggling by any technical or identity-forging means.

The camera neither cut away nor pulled back.

Two Safe Team operatives in unmarked dark-grey tactical gear stepped in from either side of the frame. The courtyard was terrifyingly quiet; the mic picked up only compressed, distorted wind, followed by a dull, muffled report.

Two bodies pitched forward onto the pale-grey concrete. Dark red liquid spread slowly along the rough grain toward a stainless-steel floor drain in the corner. The camera held its steady, restrained eye-level framing for ten full seconds.

At the very bottom of the frame, that clean, elegant warm-sand serif subtitle sat motionless.

Zhou Kuo’s phone vibrated in his palm. Mechanically, he switched back to his messaging app. Within two minutes, all three proxy-KYC brokers he had bookmarked turned into blank grey avatars, their usernames flipping in unison to `Deleted Account`.

Right before the forum mirror severed completely, a scrolling anonymous ticker along the bottom flashed one last rushed line: *Blackfeather’s Big Qi got clipped, channel boss Raven wiped his account and bolted two days ago, everyone’s purging DBs, each man for himself.*

Then the page threw a 404 and the screen went blank.

---

The wall clock pointed to 7:25.

Ninety minutes left until code freeze.

Zhou Kuo sat motionless at his desk. The room was bitterly cold; the drops of water he had spilled earlier still hadn’t dried.

Staring at that courteous white modal on his old laptop, he ran the ledger over and over in his head.

If he shut the computer now, he wouldn’t have the exception-compensation code by nine. Old Ma wouldn’t hear excuses about a busted relay, and the big boss certainly wouldn’t carry a Grey Zone programmer for an extra month just because his crutch broke. When Monday’s layoff roster went up, at thirty-two with a rusted-out first brain in a dead hiring market, he wouldn’t land another job in six months. Four months of cash, one missed mortgage payment, and the suburban apartment—already down forty percent—would go to foreclosure auction, leaving him still owing the bank after the sale, dropping straight below the Cull Line.

The grey-market KYC brokers had just lost their heads on a livestream. Every channel online was dead; nobody left would touch an order.

Only one button remained on the desk in front of him.

Zhou Kuo’s finger drifted slowly toward the trackpad. A preposterous yet strangely lucid thought surfaced in his mind: Safe Team executed relay operators and credential forgers; he was just an ordinary developer who had paid full price. Besides, this heirloom email had six clean years of Supported Region history. What if? What if the system respected account age, or at worst rejected the passport and refunded his subscription? Surely they wouldn’t lock down an entire human being’s life just for writing backend code?

He pulled open the drawer and took out his dark-red Grey Zone passport. The plastic sleeve felt slightly tacky under his fingertips.

Zhou Kuo clicked `Verify Identity`.

The green LED beside the webcam flickered on. He turned on the desk lamp, dimmed it low, and held the passport photo page up to the lens. The green framing box tightened automatically and snapped shut with a soft digital click.

Liveness verification came next. Gentle English prompts floated across the top of the warm-sand interface, like a patient nurse in an optometry clinic.

`Please turn your head slightly to the left.`

Zhou Kuo obeyed.

`Now look at the camera and blink slowly.`

Facing the lens, he blinked once, slowly.

In thirty seconds flat, he personally packaged his passport number, facial bone geometry, iris patterns, device hardware fingerprint, six-year heirloom webmail, and payment card trail, and shipped the whole bundle across the ocean into the global joint risk network.

A soft progress line appeared on screen: `Reviewing your information...`

Zhou Kuo stood up, walked to the kitchen, and poured half a glass of cold water. Leaning against the kitchen doorway with the glass in hand, he watched the clock face. One minute. Two minutes. Three minutes.

It hadn’t auto-rejected. A pathetic spark of luck flickered in his chest—maybe it had routed to manual review or a leniency queue; maybe six years of clean webmail history were buying him a pass.

Four minutes and twelve seconds.

In the background of the custom Tor Browser, the webmail tab twitched, a quiet `(1)` appearing in its title bar. In almost the exact same second, the warm-sand main tab refreshed on its own.

There were no red warning icons on the page, not a trace of reproach—just an impeccably phrased notice, word-for-word identical to the email that had just landed in his inbox.

```text
Account Suspended

Your account has been permanently disabled due to a violation of our
Regional Access and Usage Policy.

If you believe this was a mistake, you may submit a one-time appeal below.
```

Zhou Kuo’s hands began to shake. He nearly threw himself back into the chair and clicked the tiny `Submit an appeal` link at the bottom.

Scraping together the last shreds of decent English in his head, he typed out a long, nearly groveling paragraph in the appeal box. He wrote that he was just an ordinary backend engineer in a Grey Zone, had never resold API keys, had never used the model for anything illicit, only checked routine business logic, was willing to pay the full Supported Region subscription rate, and begged them to review his account history one more time.

He clicked send.

Staring at the webmail inbox, he knotted his fingers tightly together.

Eighty-three seconds later, the second email arrived.

```text
Subject: Update on your account appeal

Hello,

After careful review, we have determined that your account cannot be reinstated.
This decision is final.

Thank you for your understanding.
A\ Trust & Safety
```

Zhou Kuo read those two sentences three times. Eighty-three seconds. *After careful review.* *This decision is final.* And still so polite at the end, thanking him for his understanding.

His phone began buzzing across the tabletop, one alert after another.

The first notification came from the virtual debit card issuer: his account had been permanently frozen under joint global compliance risk controls, remaining balance forfeited.

Two minutes later, the six-year-old heirloom webmail tab logged itself out automatically, displaying a notice that the account had been permanently disabled due to high-risk regional identity association and Terms of Service violations.

One minute after that, a Supported Region cloud provider console still open on his work computer popped up a forced sign-out dialog, its error code pointing to the exact same joint biometric and document blacklist.

From start to finish, less than five minutes—clean as building management throwing the main breaker on a tenant behind on rent, leaving not even a slot to argue through.

8:04 a.m.

Zhou Kuo closed the old laptop and unplugged its power cord. He folded the dark-red passport shut, tucked it into the very back of the drawer, and slid the drawer closed.

On his main monitor, the code editor still glowed. The window sat on line 184 of `clearing_engine.go`, where a steady vertical cursor blinked at the end of a half-written `if` branch.

He rested both hands back on his mechanical keyboard, ten fingertips perched on the familiar keycaps, and for a long time did not press the first key.

Outside on the avenue, an early morning bus eased to a stop, let out a long hiss from its air brakes, and pulled away. The room was completely quiet, and so was Zhou Kuo’s mind.
