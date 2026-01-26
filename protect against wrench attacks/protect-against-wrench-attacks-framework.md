# How to Protect Against Wrench

In cases of physical aggression or violence, **immediately notify your local law enforcement**.
If crypto assets have been stolen, contact [**SEAL911**](https://securityalliance.org/our-work/seal-911).

## Overview

### What is a wrench attack?

A wrench attack is any situation where the attacker bypasses technical security by directly targeting the person who controls the keys. Unlike phishing, malware, or protocol exploits, wrench attacks assume the attacker has physical proximity or credible reach to the victim and that technical controls alone are insufficient. 

The term originates from the [*xkcd* webcomic](https://xkcd.com/538/), which satirically illustrated that sophisticated 4096-bit RSA encryption could be bypassed more effectively by a $5 wrench than by a supercomputer.


### Why does this matters now?

- Growth of self‑custody, non‑custodial wallets, and on‑chain treasuries means more value is directly controlled by a small number of individuals, often without institutional physical security.
- Public on‑chain data, social media signaling, and leaks make it easier for adversaries to identify likely high‑value targets and correlate them with real‑world identities.
- Existing wallet security guidance focuses mainly on technical compromise.

### Scope

Scope includes individuals (founders, traders, KOLs) and organizations like crypto exchanges, funds, DAOs, etc,  operating with significant on‑chain or custodial balances.

Moreover, the framework assumes that adversaries can use basic OSINT, social engineering, and physical surveillance to find and pressure key‑holders.

## Threat Model

Wrench attacks rely on coercing people, not breaking cryptography. This section characterizes who the adversaries are, what they want, and where they are most likely to strike, so that wallet and key setups can be aligned to real‑world risk instead of purely technical assumptions.

### Attacker types

- **Opportunistic criminals**
    
    Street‑level or local gangs who become aware that a target “has crypto” (through social media, lifestyle, or loose talk) and attempt fast, high‑pressure extortion with limited technical skills. These actors typically aim for immediate liquid funds (hot wallets, exchange accounts) and are more sensitive to time pressure and visible risk.
    
- **Organized crime groups**
    
    Structured groups that combine OSINT, surveillance, and insider recruitment to identify and pressure high‑value key‑holders, including founders, and treasury staff.
    
- **Insiders and close circle**
    
    Current or former employees, contractors, business partners, family members, or intimate partners who know or suspect that the victim controls significant digital assets. They often possess contextual knowledge (where devices are, when approvals happen, who else can sign), making them especially dangerous in blended social–physical attacks.
    
- **State actors**
    
    Security services, law‑enforcement units, or proxy groups in jurisdictions with weak rule of law or hostile regulatory environments, using detention, travel stops, or raids to obtain keys or force on‑chain actions.
    
### Attacker objectives
    
- **Direct theft**
    
    Forcing the victim to unlock devices, disclose seed phrases, or sign transactions to transfer funds to attacker‑controlled addresses.
    
- **Extortion and blackmail**
    
    Using threats of continued violence, exposure, or reputational damage to demand repeated payments over time. May target both personal funds and organizational treasuries.
    
- **Operational coercion**
    
    Forcing specific on‑chain actions: pausing or upgrading contracts, whitelisting addresses, approving malicious proposals, or leaking internal secrets and signing policies.
    
- **Intelligence gathering**
    
    Mapping the organization’s wallet architecture, signing processes, key‑holders, and recovery mechanisms for future operations.
    

### Attack surfaces

- **Residential environment**
    
    Home invasions, confrontations in building common areas, parking ambushes, and threats involving family members or roommates.
    
- **Workplace**
    
    Approaching treasury, operations, or engineering staff near the office, parking areas, or on their commute home. Risks increase when work devices with wallet access leave secure premises or when visitors can move freely inside office spaces.
    
- **Public spaces**
    
    Incidents in cafés, restaurants, airports, hotels, or nightlife locations where routine patterns are easy to observe. Crypto events (conferences, side‑events) are particularly attractive hunting grounds, as they densely concentrate potential targets.
    
- **Family, friends, and staff**
    
    Threats directed at spouses, partners, children, drivers, assistants, or security staff, who may have indirect access. Attackers can also use them as leverage.


## Risk factors and early signals

### Individual risk factors

**Public visibility** and signaling are among the strongest individual risk amplifiers for wrench attacks. Founders, KOLs, traders, and engineers who publicly reference large fundraising rounds, trading gains, or treasury balances substantially increase their appeal as targets. 

**Lifestyle choices** and daily routines further magnify this exposure by making physical access both predictable and low-cost. Conspicuous displays of wealth, such as luxury cars, expensive accessories, or frequent premium travel, combined with repetitive behaviors enable even rudimentary surveillance to identify favorable moments for intervention. Operating from unsecured home environments while routinely approving high-value transactions also collapses digital control and physical presence into the same space, centralizing financial risk and personal safety threats on a single individual.

### Organizational risk factors

Organizational risk factors primarily stem from concentrated key-holder power and weak separation of duties, which create high-value targets for wrench attacks. When a single individual can authorize major treasury movements, physical coercion becomes an efficient path to theft.

Poor governance exacerbates this risk by treating key management as a purely technical function, disconnected from physical security and HR oversight, leaving key exposures unaddressed during hiring, role transitions, or travel.

### Environmental and geographic risk factors

Regions with high rates of violent crime, weak law enforcement, or corruption raise the baseline probability that crypto‑related targets will be identified and approached. Travel to jurisdictions with aggressive or opaque enforcement practices increases the risk of “official” coercion at borders, hotels, or offices.

### Early signals and pre‑incident indicators

- **OSINT and probing behavior**
    
    Unusual follower spikes, repeated DMs asking operational questions, or detailed probing about treasury structure, custody, or personal routines can signal reconnaissance. Repeated appearance of unfamiliar individuals around home or office should be treated as a potential warning.
    
- **Escalating threats and doxxing**
    
    Targeted harassment, threats mentioning family, or doxxing posts linking real identity to wallet addresses or balances often precede physical attempts. Leaks of internal documents or partial leaks of residential/work addresses can also mark a shift from opportunistic to targeted risk.


## Defensive design principles

These principles guide all subsequent controls, ensuring wallet architectures and operational processes withstand coercion without relying solely on the victim's resistance under extreme pressure.

### Minimization

- Minimize the value and impact of what any single coerced individual can authorize during a time-constrained attack window.
- Design wallet tiers and signing limits so that even full compliance yields only low-to-moderate losses, forcing attackers to sustain operations longer and increasing their detection risk.

### Compartmentalization

- Segment keys, identities, devices, locations, and roles to prevent compromise of one element from cascading across the entire stack.
- Separate hot wallets for daily ops from cold storage for long-term holdings, and distribute signer responsibilities across jurisdictions, risk profiles, and access methods.

### Plausibility

- Incorporate believable decoy structures that align with the victim's public profile, such as low-value "compliance wallets" containing realistic but sacrificial balances. Decoys must appear operationally consistent to withstand basic scrutiny.

### Resilience

- Design for post-incident recovery without single points of failure.
- Protect human factors: avoid blame cycles, control information flows to prevent secondary leaks or attrition.
- Maintain operational continuity through distributed knowledge and pre-tested reconstruction.

### Prioritization

- Sequence all controls to favor human safety over assets during active threats.
- No policy incentivizes physical resistance; wallet rules yield immediately to safety triggers.
- Integrate with physical security, crisis management, and law enforcement protocols.

## Wallet and key architecture

### Wallet strategy

- **Hot wallets** (0-1% of total value)
    
    Daily operational funds on L1/L2 for gas, small payments, emergency liquidity; strict daily spend limits (<$10k equiv.), no direct path to cold storage.
    
- **Warm wallets** (1-5%)
    
    Short-term operational (1-7 days) funds for payroll, vendor payments, marketing; geo-fenced approvals, multi-sig with time delays for larger moves.
    
- **Cold wallets** (5-25%)
    
    Medium-term holdings accessible within 24-72 hours via hardware signers; stored in bank vaults or secure facilities, never at primary residence/office.
    
- **Deep-cold** (remaining balance)
    
    Strategic reserves in air-gapped HSMs, multi-party custodians, or institutional custody; recovery requires legal processes or key ceremonies spanning weeks.
    

### Multisig and MPC

- **Multisig setups**
    
    Minimum 3-of-5 or 4-of-7 signers for any material movement; distribute across geographies and risk profiles so coercing one person blocks action.
    
- **MPC (multi-party computation)**
    
    Threshold schemes where no single key share enables spending.
  

### Geographically decoupled key storage

- **Primary residence**
    
    Never store hardware wallets, seeds, or signer devices. Use only temporary hot wallet access via secure elements (YubiKey, phone-bound keys).
    
- **Secure offsite locations**
    
    Bank safety deposit boxes, private vaults, or trusted family abroad for cold wallet hardware.
    
- **Institutional custodians**
    
    Fireblocks, Copper, or regulated providers for deep-cold.
    
- **Smart contract guardians**
    
    Protocol-level treasuries use on-chain timelocks, pause functions, or emergency multi-sig for protocol upgrades under duress.
    

### Decoy and compliance wallets

- **Plausible decoy wallets**
    
    Create 2-3 secondary wallets with $2k-$5k balances matching observed transaction patterns. Seeds/PINs memorized separately for handover.
    
- **Duress codes/PINs**
    
    Secondary credentials unlock decoy wallets or trigger silent alarms/limits.
    
- **Burner exchange accounts**
    
    Pre-funded CEX accounts ($10k) linked to public personas, for immediate compliance transfers without touching core holdings.
    

### Key ceremonies and rotation policies

- **Initial key ceremonies**
    
    Conducted in neutral third-party locations with video audit trails. Mnemonic shards split across minimum 3 participants, never whole seeds.
    
- **Periodic rotations**
    
    Quarterly review of signer eligibility. Annual full key refresh with new hardware/devices. Trigger rotations after travel to high-risk jurisdictions.
    
- **Post-incident rotation**
    
    Pre-defined playbook for 24-hour signer replacement, contract migrations, and full-stack rebuild without single points of failure.

## Personal and family OpSec

OpSec shrinks the real-world attack surface by reducing what adversaries can learn about targets, their routines, and their connections to digital assets.

### Digital hygiene

- **Eliminate persistent OSINT signals**
    
    Scrub public profiles of home addresses, vehicle plates, routine locations (gyms, cafes), and geo-tagged photos; use temporary numbers/emails for non-essential accounts.
    
- **Harden devices**
    
    Full-disk encryption, no seed phrases or wallet apps on always-on phones/laptops, regular factory resets on operational devices, and no cloud sync of sensitive data.
    
- **Financial anonymity**
    
    Route crypto ops through mixers or privacy chains where legal, avoid linking exchange KYC to public social handles, use business entities for high-value holdings.
    

### Identity separation

- **Public persona vs. asset control**
    
    Maintain distinct digital identities for social presence versus wallet signing.
    
- **Compartmentalized devices**
    
    Public phone for social/travel, signer phone kept in secure location, never carried together.
    
- **Family dissociation**
    
    No joint public profiles, separate finances/devices, educate on not discussing crypto holdings or signing routines at home/social events.
    

### Family and staff training

- **Simple family protocols**
    
    *"If someone asks about money/crypto, say nothing and text [safe word] to [emergency contact]."* 
    
    Pre-rehearsed silent alarms to neighbors/security.
    
- **Staff NDAs and drills**
    
    Drivers/assistants trained to vary routes, report surveillance, never discuss boss's assets/locations. Tabletop exercises for home/office scenarios.
    
- **Children and vulnerable contacts**
    
    Age-appropriate rules like *"never open the door for strangers"* or *“never share phone screens"*, school pick-up codes, and emergency family assembly points.
    

### Physical routine hardening

- **Unpredictability**
    
    Rotate gyms/cafes/commutes weekly, avoid solo night outings, use ride-shares with fake names/locations, never carry >$2k cash/cards visibly.
    
- **Home defenses**
    
    Reinforced doors/windows, cameras with remote alerts, safe rooms, no visible luxury goods or crypto-branded items.
    
- **Travel hardening**
    
    No wallet signing during trips, inform trusted contacts of itineraries, use hotel safes for devices, avoid high-profile events solo.
    

### Social engineering resistance

- **Standard responses to probes**
    
    *"I don't handle that"* or "*Ask my lawyer/colleagues"* for any crypto questions. Never confirm or deny holdings.
    
- **Fake stories**
    
    Plausible cover narratives like *"Everything's in custody"* or *"Team handles treasury"* consistent across family/staff to deflect without raising suspicion.
    
- **Regular audits**
    
    Quarterly review of social profiles, on-chain links to identities, and staff access by external security consultants.

## Transaction flows under duress

### Hard limits and friction

- Enforce per-transaction limits and daily limits on hot and warm wallets so coerced actions cannot drain strategic reserves in one sitting.
- Require additional approvals once a transfer crosses predefined thresholds, even if the request looks operationally normal.
- Prefer time delays for larger movements so that an attacker must sustain control for longer, increasing the chance of interruption.

### Separation of approval channels

- Ensure the request and approval path are on different devices and ideally different people, so coercing one operator does not complete the full flow.
- Keep high-privilege signing devices physically separated from day-to-day devices used in public or during travel.
- Use geodiversity for signers so a local incident cannot immediately compel all required approvals.

### Duress-compatible operating modes

- Maintain a plausible, low-value compliance path that can satisfy an attacker quickly without exposing core funds.
- Keep that compliance path consistent with the target’s profile and normal activity so it can withstand basic scrutiny during coercion.
- Make sure the compliance path has no direct upgrade route to higher tiers.

### High-risk period tightening

- During travel temporarily lower limits and increase required approvals by policy.
- Treat credible threats, doxxing, or surveillance indicators as triggers to move operations into a heightened security mode with reduced transaction capability.

## Scenario playbooks

This section analyzes real-world attack scenarios to demonstrate where security controls succeed or fail, providing actionable preparation for both organizations and individuals.

### Scenario 1: Targeted home invasion of a founder

**Profile**: 

Public founder or high-net-worth individual with visible crypto holdings, active on social media, predictable home routine.

**Attack sequence**:

Adversaries use OSINT to identify home address, vehicle, and daily patterns. They conduct multi-day surveillance to confirm routines and household composition. Attack occurs during evening or late in the night when family is present, using multiple armed actors to control the scene quickly. Victims are forced to unlock devices, transfer funds from hot/cold wallets, or reveal seed phrases under threats to family members.

**Common failure modes**:

- Hot wallets on personal devices with no transaction limits accessible from home.
- Hardware wallets or written seeds stored in obvious home locations.
- No duress protocols or decoy wallets, forcing victim to either resist or hand over everything.
- Family members unaware of protocols, escalating panic and attacker frustration.

**Effective controls**:

- Zero high-privilege signing devices at primary residence.
- Prepared decoy wallet with memorized PIN, realistic transaction history.
- Family trained on silent alarm codes and safe room protocols.
- Cold/deep-cold storage requires bank vault access or multi-party approval impossible to complete under duress.

### Scenario 2: Kidnapping and sustained coercion abroad

**Profile**: 

Founder, executive, or trader traveling to conference or business meeting.

**Attack sequence**:

Target doxxed via conference attendee lists, social posts, or leaked travel itineraries. Adversaries approach via dating apps, fake business meetings, or direct abduction from hotel/venue. Victim held for hours to days, subjected to escalating coercion (torture, mutilation) to force multi-tier wallet access.

**Common failure modes**:

- Traveling with full signing authority and devices for operational continuity during trip.
- No geo-restricted policies preventing high-value transactions from abroad.
- No pre-defined incident protocols for sustained coercion scenarios.

**Effective controls**:

- Zero signing authority during travel. Temporary operational limits enforced by smart contract or multisig rules.
- Geofencing on wallet approvals. High-value transactions should be blocked from foreign IPs/locations.
- Decoy compliance path gives attacker something while buying time for rescue.

### Scenario 3: Insider-enabled coercion of treasury staff

**Profile**: 

Operations or treasury staff with multisig authority, targeted by former employee, contractor, or family member with insider knowledge.

**Attack sequence**:

Insider leaks home address, device types, etc, to external criminals. Victim pressured to approve specific prepared transactions that appear operationally normal. Insider may also provide attacker with plausible cover story or fake urgency to bypass colleague scrutiny.

**Common failure modes**:

- Single staff member can unilaterally approve material payments without real-time peer review.
- Signing happens from home or remote locations with no audit trail or secondary verification.
- Insider knowledge of bypass procedures.

**Effective controls**:

- All material transactions require synchronous multi-party approval with voice/video verification.
- Signing limited to office hours from secure facility.
- Transaction pattern monitoring flags unusual timing, amounts, or beneficiary addresses.
- Insider threat program with regular access reviews, exit interviews with key rotation, NDAs with enforcement.
- Staff authorized to refuse under any pressure; refusal never results in penalty.


## Incident response

Wrench-attack incident response must prioritize human safety first, while rapidly containing any ability to move funds or coerce additional signers. 

### Immediate triage

- Treat it as a life-safety emergency first, and assume the victim may still be under observation or ongoing coercion.
- Activate a pre-defined crisis channel and a single incident commander to avoid fragmented decisions and conflicting instructions.
- Make an initial determination of what the attacker likely obtained.

### De-escalation

- Do not instruct actions that could escalate violence while the victim is under direct threat.
- Move the victim (and family, if relevant) to a safe location and coordinate medical care, then transition to controlled debriefing once stable.
- If travel-related, assume device seizure or border detention dynamics and involve local legal support immediately.

### Technical containment

- Signer rotation, disabling compromised signers, and migrating funds from exposed tiers to contingency wallets.
- If smart contracts are in scope, consider pausing, timelocking, or restricting privileged functions to prevent coercion-driven upgrades or admin actions.
- Assume all secrets on any unlocked device are compromised, and rebuild from clean hardware with new credentials.

### Coordination with external parties

- Contact custodians, exchanges, and key infrastructure vendors via established escalation paths to block suspicious movements and document actions taken.
- Engage law enforcement through counsel and crisis-management support to preserve victim safety and handle reporting in a way that does not increase risk.
- If insurance is relevant, notify per policy requirements while controlling operational details that could leak sensitive signer or location information.

### Evidence and decision logging

- Preserve transaction hashes, timestamps, communications, and device state information to support investigations and recovery actions.
- Maintain a secure incident log of decisions, approvals, and containment steps to enable post-incident audit and prevent confusion across teams.
- Limit internal distribution of sensitive incident details to a strict need-to-know group to reduce secondary leakage and follow-on targeting.

### Post-incident actions

- Conduct a controlled post-mortem that covers both wallet architecture weaknesses and physical/OSINT exposure, then implement prioritized remediation.
- Refresh the entire key-management posture: new signer sets, revised limits, updated travel rules, and retraining for high-risk roles.
- Provide structured support for affected individuals (time off, security upgrades, relocation support when necessary) to reduce further harm and stabilize operations.

## Recovery and resilience

Recovery focuses on safely restoring trust in the wallet infrastructure and supporting the people affected. Resilience means learning from the event to harden the entire system against future coercion attempts.

### Human factors

- Provide psychological support and professional counseling for victims and their families.
- Assess whether the targeted individual can realistically continue in a key-holding role given their heightened profile and potential ongoing risk.
- Address broader team morale and fear by communicating clearly about new security measures and support resources.

### Infrastructure reconstruction

- Do not reuse any seed phrases, private keys, or devices that were physically accessible during the incident, even if they appear untouched.
- Build a new wallet hierarchy from scratch and migrate remaining assets only after validating the new setup.
- Re-verify all multisig participants, threshold settings, and allowlists to ensure no attacker-controlled addresses or signers were inserted during the compromise.

### Governance

- Revise travel, remote-work, and high-value transaction policies to close specific gaps exploited in the attack.
- Formalize “lessons learned” into the risk register and training materials so new team members understand why specific constraints exist.

### Long-term monitoring

- Implement enhanced monitoring for the affected individuals and new wallet addresses to detect any persistent surveillance or follow-on attempts.
- Periodically re-assess the threat landscape to ensure the recovered posture remains effective over time.
- Maintain a relationship with threat intelligence and physical security partners to stay ahead of evolving coercion techniques targeting the sector.

## Checklist

This checklist translates the framework into concrete actions, divided by implementation phase and entity type, to help prioritize deployment.

### Maturity assessment

- **Basic** (High Risk): Single-factor cold storage, no daily limits, ad-hoc signing, high public visibility.
- **Intermediate** (Medium Risk): Multisig/MPC for treasury, basic limits, separate signing devices, some staff training.
- **Advanced** (Low Risk): Geo-distributed keys, strict role separation, decoy protocols, regular drills, 24/7 monitoring.

### Immediate hardening (Day 1-7)

**Individual**:

- [ ]  Remove all wallet apps, seeds, and screenshots from daily-driver phones and laptops.
- [ ]  Set strict daily spending limits on hot wallets (<$10k equiv.) and move excess to cold storage.
- [ ]  Create one "plausible decoy" wallet with a small, realistic balance and memorize its access PIN.
- [ ]  Audit home/office for visible hardware wallets or recovery sheets and move them to secure storage.

**Organization**:

- [ ]  Audit all active signers.
- [ ]  Verify that no single person can unilaterally move >1-5% of treasury assets without a second approver.
- [ ]  Brief key staff on "safety first" protocols.

### Structural architecture (Month 1-3)

**Individual**:

- [ ]  Separate "public identity" digital footprint from "asset control" identity.
    - [ ]  Dedicated email
    - [ ]  SIM and phone
    - [ ]  Device
- [ ]  Establish a cold storage tier (multisig or MPC) where keys are geographically separated.
- [ ]  Implement a "duress code" or panic protocol with a trusted contact or security service.
    - [ ]  Trusted contact
    - [ ]  Security Service

**Organization**:

- [ ]  Deploy a tiered wallet architecture (Hot/Warm/Cold) with automated limits and defined purpose per tier.
- [ ]  Implement MPC or Multisig with geographic and role-based distribution (e.g., Legal + Finance + Ops).
- [ ]  Formalize the "Key Ceremony" process for generating and backing up new operational keys.
- [ ]  Integrate wallet security training into onboarding for ALL staff.

### Advanced resilience (Month 3-6+)

**Individual**:

- [ ]  Conduct a full OSINT cleanup of personal data:
    - [ ]  Home address
    - [ ]  Family details
    - [ ]  Travel patterns
    - [ ]  Social medias
- [ ]  Establish a relationship with a physical security provider for travel risk assessments and monitoring.
- [ ]  Set up a formal legal structure (Trust/LLC) to obscure asset ownership where possible.

**Organization**:

Run quarterly tabletop exercises simulating coercion, kidnapping, and insider threats.

- [ ]  Implement real-time transaction monitoring and anomaly detection for treasury wallets.
- [ ]  Establish a retained incident response relationship with crypto-specialized investigators/negotiators.
- [ ]  Conduct third-party penetration tests targeting technical infrastructure.
- [ ]  Conduct third-party penetration tests targeting staff social engineering.

## More resources

Here you will find more valuable resources to dig further:

[Securing Cryptocurrency Organizations | Google Cloud Blog](https://cloud.google.com/blog/topics/threat-intelligence/securing-cryptocurrency-organizations/?hl=en)

[Wrench attacks: A closer look at prevalence and prevention - Unchained](https://www.unchained.com/blog/wrench-attacks)

[SEAL Framework](https://frameworks.securityalliance.org/intro/introduction)

[Physical Violence In Crypto](https://stats.glok.me/)

[Physical Security Checklist](https://glok.me/checklist/download-pdf/)
