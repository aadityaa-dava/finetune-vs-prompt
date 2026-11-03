# Test-set error examples (post-hoc)

## LoRA r8 by category

### invalid JSON (sentences) (1)
- TEXT: We report here on a heretofore undescribed respiratory syncytial virus (RSV) infection in a patient with a long-standing history of refractory CLL that was treated with fludarabine phosphate.
  - GOLD: [('fludarabine phosphate', 'respiratory syncytial virus (rsv) infection')]
  - PRED: RAW END: darabine phosphate", "effect": "respiratory syncytial virus (RSV") infection"}]}

### FP: wording not in sentence (12)
- TEXT: A high dose of cotrimoxazole induced hyperkalaemia with the elevation of serum creatinine and blood urea, and increased urinary N-acetyl glucosaminase after several days of the drug administration in these patients; one patient became unconscious.
  - GOLD: [('cotrimoxazole', 'elevation of serum creatinine and blood urea'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase'), ('cotrimoxazole', 'one patient became unconscious')]
  - PRED: [('cotrimoxazole', 'elevation of serum creatinine'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased blood urea'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase')]
- TEXT: We report 2 patients who developed polyarteritis nodosa following vaccination against hepatitis B.
  - GOLD: [('vaccination against hepatitis b', 'polyarteritis nodosa')]
  - PRED: [('hepatitis b vaccination', 'polyarteritis nodosa')]
- TEXT: Recent studies have shown that under experimental conditions ferrous sulfate may reduce the gastrointestinal absorption of orally administered levothyroxine sodium in patients with primary hypothyroidism.
  - GOLD: [('ferrous sulfate', 'reduce the gastrointestinal absorption of orally administered levothyroxine sodium')]
  - PRED: [('ferrous sulfate', 'reduced the gastrointestinal absorption of orally administered levothyroxine sodium')]
- TEXT: A patient receiving vancomycin for a serious staphylococcal infection had a lupus-like syndrome characterized by a malar rash, pain and erythema of the cartilage of both ears, and tender erythematous and hemorrhagic lesions of the finger tips.
  - GOLD: [('vancomycin', 'erythema of the cartilage of both ears'), ('vancomycin', 'hemorrhagic lesions of the finger tips'), ('vancomycin', 'lupus-like syndrome'), ('vancomycin', 'malar rash'), ('vancomycin', 'pain'), ('vancomycin', 'tender erythematous')]
  - PRED: [('vancomycin', 'malar rash'), ('vancomycin', 'pain and erythema of the cartilage of both ears'), ('vancomycin', 't lupus-like syndrome'), ('vancomycin', 'tender erythematous and hemorrhagic lesions of the finger tips')]
- TEXT: Since the thrombocyte count started to increase immediately after initiation and dropped immediately after discontinuation of ciprofloxacin and tazobactam/piperacillin and all other drugs were discontinued already before or were started after the nadir of the thrombocyte count, these two antibiotics were regarded causative.
  - GOLD: [('ciprofloxacin', 'thrombocyte count started to increase'), ('piperacillin', 'thrombocyte count started to increase'), ('tazobactam', 'thrombocyte count started to increase')]
  - PRED: [('ciprofloxacin', 'thrombocyte count increased'), ('piperacillin', 'thrombocyte count increased'), ('tazobactam', 'thrombocyte count increased')]
- TEXT: Since the thrombocyte count started to increase immediately after initiation and dropped immediately after discontinuation of ciprofloxacin and tazobactam/piperacillin and all other drugs were discontinued already before or were started after the nadir of the thrombocyte count, these two antibiotics were regarded causative.
  - GOLD: [('ciprofloxacin', 'thrombocyte count started to increase'), ('piperacillin', 'thrombocyte count started to increase'), ('tazobactam', 'thrombocyte count started to increase')]
  - PRED: [('ciprofloxacin', 'thrombocyte count increased'), ('piperacillin', 'thrombocyte count increased'), ('tazobactam', 'thrombocyte count increased')]

### FP: boundary mismatch (94)
- TEXT: We present a 46-year-old African-American man with AIDS who was admitted on two different occasions within three weeks for signs and symptoms of meningitis after using trimethoprim/sulfamethoxazole (TMP/SMX).
  - GOLD: [('smx', 'meningitis'), ('sulfamethoxazole', 'meningitis'), ('tmp', 'meningitis'), ('trimethoprim', 'meningitis')]
  - PRED: [('tmp/smx', 'meningitis'), ('trimethoprim/sulfamethoxazole', 'meningitis')]
- TEXT: We present a 46-year-old African-American man with AIDS who was admitted on two different occasions within three weeks for signs and symptoms of meningitis after using trimethoprim/sulfamethoxazole (TMP/SMX).
  - GOLD: [('smx', 'meningitis'), ('sulfamethoxazole', 'meningitis'), ('tmp', 'meningitis'), ('trimethoprim', 'meningitis')]
  - PRED: [('tmp/smx', 'meningitis'), ('trimethoprim/sulfamethoxazole', 'meningitis')]
- TEXT: A high dose of cotrimoxazole induced hyperkalaemia with the elevation of serum creatinine and blood urea, and increased urinary N-acetyl glucosaminase after several days of the drug administration in these patients; one patient became unconscious.
  - GOLD: [('cotrimoxazole', 'elevation of serum creatinine and blood urea'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase'), ('cotrimoxazole', 'one patient became unconscious')]
  - PRED: [('cotrimoxazole', 'elevation of serum creatinine'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased blood urea'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase')]
- TEXT: A 25-year-old woman sought medical attention because of iliocaval manifestations of retroperitoneal fibrosis while she was taking methysergide.
  - GOLD: [('methysergide', 'retroperitoneal fibrosis')]
  - PRED: [('methysergide', 'iliocaval manifestations of retroperitoneal fibrosis')]
- TEXT: Two patients with HLH developed etoposide-related secondary acute myeloid leukemia (sAML) following therapy for HLH.
  - GOLD: [('etoposide', 'saml'), ('etoposide', 'secondary acute myeloid leukemia')]
  - PRED: [('etoposide', 'aml'), ('etoposide', 'saml')]
- TEXT: MATERIALS AND METHODS: We present two cases of significant morbidity related to primary and secondary perforation of the bladder following two instillations of epirubicin.
  - GOLD: [('epirubicin', 'primary and secondary perforation of the bladder')]
  - PRED: [('epirubicin', 'perforation of the bladder')]

### FP: wrong pairing (1)
- TEXT: ADH hypersecretion in relation to plasma osmolality was reversed by mizoribin withdrawal, suggesting that bredinin might adversely induce SIADH.
  - GOLD: [('bredinin', 'siadh'), ('mizoribin', 'adh hypersecretion')]
  - PRED: [('mizoribin', 'siadh')]

### FP: extra/unlabeled pair (47)
- TEXT: We report a case of hepatolithiasis (intrahepatic stone) complicated by gram-negative sepsis in a 37 year old male with acromegaly being treated with octreotide.
  - GOLD: [('octreotide', 'hepatolithiasis')]
  - PRED: [('octreotide', 'gram-negative sepsis'), ('octreotide', 'hepatolithiasis')]
- TEXT: CASE SUMMARIES: Two patients with stable hypothyroidism experienced symptoms of hypothyroidism with increased serum thyroid-stimulating hormone (TSH) concentrations after switching from 1 levothyroxine product to another.
  - GOLD: [('levothyroxine', 'increased serum thyroid-stimulating hormone')]
  - PRED: [('levothyroxine', 'hypothyroidism'), ('levothyroxine', 'increased serum thyroid-stimulating hormone'), ('levothyroxine', 'tsh')]
- TEXT: CASE SUMMARIES: Two patients with stable hypothyroidism experienced symptoms of hypothyroidism with increased serum thyroid-stimulating hormone (TSH) concentrations after switching from 1 levothyroxine product to another.
  - GOLD: [('levothyroxine', 'increased serum thyroid-stimulating hormone')]
  - PRED: [('levothyroxine', 'hypothyroidism'), ('levothyroxine', 'increased serum thyroid-stimulating hormone'), ('levothyroxine', 'tsh')]
- TEXT: We suggest that nicotinic acid was the cause of his liver disease, that this case is of particular note because of the rather short period of therapy before the onset of liver injury and the severity of the hepatic failure, and that the probable increased use of nicotinic acid for serum cholesterol control makes it especially important for physicians and their patients to be alert to the signs of hepatotoxicity.
  - GOLD: [('nicotinic acid', 'hepatotoxicity'), ('nicotinic acid', 'liver disease')]
  - PRED: [('nicotinic acid', 'hepatic failure'), ('nicotinic acid', 'liver disease')]
- TEXT: Mechanisms and triggering factors of hypoglycaemia induced by mefloquine and some other anti-malarial quinine analogues are discussed.
  - GOLD: [('mefloquine', 'hypoglycaemia')]
  - PRED: [('mefloquine', 'hypoglycaemia'), ('quinine', 'hypoglycaemia')]
- TEXT: CONCLUSIONS: Cicatrization in the substantia propria of the conjunctiva by excessive lymphocytic infiltration after topically administered antiglaucoma drugs including dipivefrin is a possible mechanism of action for entropion.
  - GOLD: [('dipivefrin', 'entropion')]
  - PRED: [('dipivefrin', 'cicatrization'), ('dipivefrin', 'entropion')]

### FN: boundary mismatch (109)
- TEXT: We present a 46-year-old African-American man with AIDS who was admitted on two different occasions within three weeks for signs and symptoms of meningitis after using trimethoprim/sulfamethoxazole (TMP/SMX).
  - GOLD: [('smx', 'meningitis'), ('sulfamethoxazole', 'meningitis'), ('tmp', 'meningitis'), ('trimethoprim', 'meningitis')]
  - PRED: [('tmp/smx', 'meningitis'), ('trimethoprim/sulfamethoxazole', 'meningitis')]
- TEXT: We present a 46-year-old African-American man with AIDS who was admitted on two different occasions within three weeks for signs and symptoms of meningitis after using trimethoprim/sulfamethoxazole (TMP/SMX).
  - GOLD: [('smx', 'meningitis'), ('sulfamethoxazole', 'meningitis'), ('tmp', 'meningitis'), ('trimethoprim', 'meningitis')]
  - PRED: [('tmp/smx', 'meningitis'), ('trimethoprim/sulfamethoxazole', 'meningitis')]
- TEXT: We present a 46-year-old African-American man with AIDS who was admitted on two different occasions within three weeks for signs and symptoms of meningitis after using trimethoprim/sulfamethoxazole (TMP/SMX).
  - GOLD: [('smx', 'meningitis'), ('sulfamethoxazole', 'meningitis'), ('tmp', 'meningitis'), ('trimethoprim', 'meningitis')]
  - PRED: [('tmp/smx', 'meningitis'), ('trimethoprim/sulfamethoxazole', 'meningitis')]
- TEXT: We present a 46-year-old African-American man with AIDS who was admitted on two different occasions within three weeks for signs and symptoms of meningitis after using trimethoprim/sulfamethoxazole (TMP/SMX).
  - GOLD: [('smx', 'meningitis'), ('sulfamethoxazole', 'meningitis'), ('tmp', 'meningitis'), ('trimethoprim', 'meningitis')]
  - PRED: [('tmp/smx', 'meningitis'), ('trimethoprim/sulfamethoxazole', 'meningitis')]
- TEXT: A high dose of cotrimoxazole induced hyperkalaemia with the elevation of serum creatinine and blood urea, and increased urinary N-acetyl glucosaminase after several days of the drug administration in these patients; one patient became unconscious.
  - GOLD: [('cotrimoxazole', 'elevation of serum creatinine and blood urea'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase'), ('cotrimoxazole', 'one patient became unconscious')]
  - PRED: [('cotrimoxazole', 'elevation of serum creatinine'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased blood urea'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase')]
- TEXT: A 25-year-old woman sought medical attention because of iliocaval manifestations of retroperitoneal fibrosis while she was taking methysergide.
  - GOLD: [('methysergide', 'retroperitoneal fibrosis')]
  - PRED: [('methysergide', 'iliocaval manifestations of retroperitoneal fibrosis')]

### FN: missed entirely (67)
- TEXT: The biochemistry of paracetamol hepatotoxicity is outlined and the increased susceptibility of alcoholic patients to the hepatotoxic effects of paracetamol is remarked upon.
  - GOLD: [('paracetamol', 'hepatotoxic effects'), ('paracetamol', 'hepatotoxicity')]
  - PRED: [('paracetamol', 'hepatotoxicity')]
- TEXT: A high dose of cotrimoxazole induced hyperkalaemia with the elevation of serum creatinine and blood urea, and increased urinary N-acetyl glucosaminase after several days of the drug administration in these patients; one patient became unconscious.
  - GOLD: [('cotrimoxazole', 'elevation of serum creatinine and blood urea'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase'), ('cotrimoxazole', 'one patient became unconscious')]
  - PRED: [('cotrimoxazole', 'elevation of serum creatinine'), ('cotrimoxazole', 'hyperkalaemia'), ('cotrimoxazole', 'increased blood urea'), ('cotrimoxazole', 'increased urinary n-acetyl glucosaminase')]
- TEXT: Two patients with HLH developed etoposide-related secondary acute myeloid leukemia (sAML) following therapy for HLH.
  - GOLD: [('etoposide', 'saml'), ('etoposide', 'secondary acute myeloid leukemia')]
  - PRED: [('etoposide', 'aml'), ('etoposide', 'saml')]
- TEXT: We suggest that nicotinic acid was the cause of his liver disease, that this case is of particular note because of the rather short period of therapy before the onset of liver injury and the severity of the hepatic failure, and that the probable increased use of nicotinic acid for serum cholesterol control makes it especially important for physicians and their patients to be alert to the signs of hepatotoxicity.
  - GOLD: [('nicotinic acid', 'hepatotoxicity'), ('nicotinic acid', 'liver disease')]
  - PRED: [('nicotinic acid', 'hepatic failure'), ('nicotinic acid', 'liver disease')]
- TEXT: Rofecoxib, used for dysmenorrhea, caused a herpetiform fixed drug eruption predominantly involving the lips with classic clinical and histological findings in a red-brown lesion on the dorsal hand.
  - GOLD: [('rofecoxib', 'herpetiform fixed drug eruption'), ('rofecoxib', 'red-brown lesion')]
  - PRED: [('rofecoxib', 'herpetiform fixed drug eruption')]
- TEXT: We report 2 patients who developed polyarteritis nodosa following vaccination against hepatitis B.
  - GOLD: [('vaccination against hepatitis b', 'polyarteritis nodosa')]
  - PRED: [('hepatitis b vaccination', 'polyarteritis nodosa')]

## LoRA right, 120B wrong
- TEXT: Fatal interstitial pneumonitis associated with docetaxel administration in a patient with hormone-refractory prostate cancer.
  - GOLD: [('docetaxel', 'fatal interstitial pneumonitis')]
  - 120B: [('docetaxel', 'interstitial pneumonitis')]
- TEXT: Gelofusine allergy--the need for identification jewellery.
  - GOLD: [('gelofusine', 'gelofusine allergy')]
  - 120B: [('gelofusine', 'allergy')]
- TEXT: This paper reports an autopsy case of a 78-year-old male with multiple nodules in the liver developed after long-termed administration of phosphate diethylstilbestrol (PDES) for prostatic cancer.
  - GOLD: [('pdes', 'multiple nodules in the liver'), ('phosphate diethylstilbestrol', 'multiple nodules in the liver')]
  - 120B: [('phosphate diethylstilbestrol', 'multiple nodules in the liver')]
- TEXT: We report a case of reversible DKA and new-onset DM that developed in a demented patient who was treated with quetiapine for 14 days.
  - GOLD: [('quetiapine', 'dka'), ('quetiapine', 'dm')]
  - 120B: [('quetiapine', 'new-onset dm'), ('quetiapine', 'reversible dka')]
- TEXT: We report the first case of an acute flare of eosinophilic cystitis in a 51-year-old woman after bladder instillation with dimethyl sulfoxide (DMSO) for presumed interstitial cystitis.
  - GOLD: [('dimethyl sulfoxide', 'eosinophilic cystitis'), ('dmso', 'eosinophilic cystitis')]
  - 120B: [('dimethyl sulfoxide', 'acute flare of eosinophilic cystitis')]
- TEXT: Can propofol precipitate pancreatitis in patients with Cushing's syndrome?
  - GOLD: [('propofol', 'pancreatitis')]
  - 120B: []
- TEXT: After 39 hours on argatroban, the infusion was stopped when minor bleeding was observed with a concurrent activated partial thromboplastin time (aPTT) of 100 seconds.
  - GOLD: [('argatroban', 'bleeding')]
  - 120B: [('argatroban', 'minor bleeding')]
- TEXT: RESULTS: The estimated number of Accutane prescriptions for reproductive-aged women has more than doubled in the past 10 years; it is the most widely used teratogenic drug in the United States, with approximately 2.5 per 1,000 reproductive-aged women exposed to Accutane in 1999.
  - GOLD: [('accutane', 'teratogenic')]
  - 120B: []

## 120B right, LoRA wrong
- TEXT: A 25-year-old woman sought medical attention because of iliocaval manifestations of retroperitoneal fibrosis while she was taking methysergide.
  - GOLD: [('methysergide', 'retroperitoneal fibrosis')]
  - LoRA: [('methysergide', 'iliocaval manifestations of retroperitoneal fibrosis')]
- TEXT: A case of recall pneumonitis induced by gemcitabine is reported.
  - GOLD: [('gemcitabine', 'recall pneumonitis')]
  - LoRA: [('gemcitabine', 'pneumonitis')]
- TEXT: Acute sensorineural hearing loss following intravenous ketoralac administration.
  - GOLD: [('ketoralac', 'acute sensorineural hearing loss')]
  - LoRA: [('ketoralac', 'sensorineural hearing loss')]
- TEXT: OBJECTIVE: To investigate the mechanisms involved in hypersensitivity reactions to cyclosporine and determine the feasibility of future cyclosporine use.
  - GOLD: [('cyclosporine', 'hypersensitivity reactions')]
  - LoRA: [('cyclosporine', 'hypersensitivity')]
- TEXT: Mechanisms and triggering factors of hypoglycaemia induced by mefloquine and some other anti-malarial quinine analogues are discussed.
  - GOLD: [('mefloquine', 'hypoglycaemia')]
  - LoRA: [('mefloquine', 'hypoglycaemia'), ('quinine', 'hypoglycaemia')]
- TEXT: We report a 13 year-old male who developed life-threatening anaphylaxis early in the course of Increlex therapy.
  - GOLD: [('increlex', 'anaphylaxis')]
  - LoRA: [('increlex', 'life-threatening anaphylaxis')]
- TEXT: CONCLUSIONS: Cicatrization in the substantia propria of the conjunctiva by excessive lymphocytic infiltration after topically administered antiglaucoma drugs including dipivefrin is a possible mechanism of action for entropion.
  - GOLD: [('dipivefrin', 'entropion')]
  - LoRA: [('dipivefrin', 'cicatrization'), ('dipivefrin', 'entropion')]
- TEXT: Restless legs syndrome and periodic limb movements during sleep probably associated with olanzapine.
  - GOLD: [('olanzapine', 'periodic limb movements during sleep'), ('olanzapine', 'restless legs syndrome')]
  - LoRA: [('olanzapine', 'periodic limb movements'), ('olanzapine', 'restless legs syndrome')]
