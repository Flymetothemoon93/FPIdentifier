import csv

def generate_report(input_file, output_file):
    # Define transposon protein InterPro IDs and descriptions
    transposon_interpro_ids = {
    "IPR000123": "RNA-directed DNA polymerase (reverse transcriptase), msDNA",
    "IPR000477": "Reverse transcriptase domain",
    "IPR000840": "Gamma-retroviral matrix protein",
    "IPR001037": "Integrase, C-terminal, retroviral",
    "IPR001207": "Transposase, mutator type",
    "IPR001352": "Ribonuclease HII/HIII",
    "IPR001598": "Transposase, IS30, conserved site",
    "IPR001959": "Probable transposase, IS891/IS1136/IS1341",
    "IPR002079": "Gag polyprotein, inner coat protein p12",
    "IPR002156": "Ribonuclease H domain",
    "IPR002492": "Transposase, Tc1-like",
    "IPR002513": "Tn3 transposase DDE domain",
    "IPR002514": "Transposase IS3/IS911family",
    "IPR002525": "Transposase IS110-like, N-terminal",
    "IPR002559": "Transposase IS4-like domain",
    "IPR002560": "Transposase IS204/IS1001/IS1096/IS1165, DDE domain",
    "IPR002622": "Transposase, Synechocystis PCC 6803",
    "IPR002686": "Transposase IS200-like",
    "IPR003036": "Core shell protein Gag P30",
    "IPR003201": "Transposase Tn5, dimerisation",
    "IPR003346": "Transposase IS116/IS110/IS902, C-terminal",
    "IPR004191": "Integrase, Tn916-type, N-terminal DNA binding",
    "IPR004291": "Transposase IS66, central domain",
    "IPR004312": "Arabidopsis retrotransposon Orf1, C-terminal",
    "IPR004875": "DDE superfamily endonuclease domain",
    "IPR005063": "Transposase, IS1",
    "IPR005162": "Retrotransposon gag domain",
    "IPR006783": "Transposase, ISC1217",
    "IPR006842": "Transposase (putative), YhgA-like",
    "IPR007069": "Transposase, IS801/IS1294",
    "IPR007321": "Transposase (putative), gypsy type",
    "IPR008042": "Retrotransposon, Pao",
    "IPR008490": "Transposase InsH, N-terminal",
    "IPR008878": "Transposase IS66, Orf2",
    "IPR009004": "Transposase, Mu, C-terminal",
    "IPR009882": "Gypsy",
    "IPR010998": "Integrase/recombinase, N-terminal",
    "IPR010999": "Retroviral matrix protein",
    "IPR011320": "Ribonuclease H1, N-terminal",
    "IPR011518": "Transposase, Rhodopirellula-type",
    "IPR011946": "Integrase, integron-type",
    "IPR012337": "Ribonuclease H-like superfamily",
    "IPR013103": "Reverse transcriptase, RNA-dependent DNA polymerase",
    "IPR014735": "Transposase, Tn5-like, N-terminal",
    "IPR014737": "Transposase, Tn5-like, C-terminal",
    "IPR014817": "Gag protein p6",
    "IPR015122": "Excisionase from transposon Tn916",
    "IPR015378": "Transposase-like, Mu, C-terminal",
    "IPR017894": "HTH domain, IS21 transposase-type",
    "IPR017895": "Helix-turn-helix, IS408/IS1162 transposase-type",
    "IPR018289": "MULE transposase domain",
    "IPR018290": "MULE transposase, N-terminal all-beta domain",
    "IPR021027": "Transposase, putative, helix-turn-helix domain",
    "IPR022242": "Transposable element P transposase-like, C-terminal",
    "IPR022892": "Ribonuclease HI",
    "IPR024442": "Transposase, zinc-ribbon",
    "IPR024445": "ISXO2-like transposase domain",
    "IPR024463": "Transposase TnpC, homeodomain",
    "IPR024473": "Transposase, IS4, N-terminal",
    "IPR024474": "Transposase IS66, zinc-finger binding domain of",
    "IPR024567": "Ribonuclease HII/HIII domain",
    "IPR024650": "Peptidase A2B, Ty3 transposon peptidase",
    "IPR025124": "Gag1-like, clamp domain",
    "IPR025166": "Integrase, DNA-binding domain",
    "IPR025246": "Transposase IS30-like HTH domain",
    "IPR025476": "Helitron helicase-like domain",
    "IPR025525": "hAT-like transposase, RNase-H fold",
    "IPR025668": "Transposase DDE domain",
    "IPR025960": "Reverse transcriptase, N-terminal domain",
    "IPR026889": "Transposase zinc-binding domain",
    "IPR027805": "Transposase, Helix-turn-helix domain",
    "IPR027806": "Harbinger transposase-derived nuclease domain",
    "IPR028350": "DNA replication protein DnaC/insertion sequence IstB-like",
    "IPR029261": "Transposase IS204/IS1001/IS1096/IS1165, zinc-finger",
    "IPR029472": "Retrotransposon Copia-like, N-terminal",
    "IPR029526": "PiggyBac transposable element-derived protein",
    "IPR031906": "Regulator of Ty1 transposition protein 107, BRCT domain",
    "IPR032718": "PiggyBac transposable element-derived protein 4, C-terminal zinc-finger domain",
    "IPR032874": "DDE domain",
    "IPR032877": "Transposase IS204/IS1001/IS1096/IS1165, helix-turn-helix domain",
    "IPR035300": "L1 transposable element, dsRBD-like domain",
    "IPR035301": "L1 transposable element, trimerization domain",
    "IPR036397": "Ribonuclease H superfamily",
    "IPR036515": "Transposase IS200-like superfamily",
    "IPR036862": "Integrase, C-terminal domain superfamily, retroviral",
    "IPR036946": "Gamma-retroviral matrix domain superfamily",
    "IPR037056": "Ribonuclease H1, N-terminal domain superfamily",
    "IPR038215": "Transposase, Tn5-like, N-terminal domain superfamily",
    "IPR038717": "Tc1-like transposase, DDE domain",
    "IPR038720": "YprB, ribonuclease H-like domain",
    "IPR038721": "Transposase IS701-like, DDE domain",
    "IPR039266": "Autonomous transposable element EN-1 mosaic protein",
    "IPR039464": "Gag-Pol polyprotein, Zinc-finger like domain",
    "IPR039537": "Retrotransposon Ty1/copia-like",
    "IPR039552": "Transposase IS66, C-terminal",
    "IPR041373": "Reverse transcriptase, RNase H-like domain",
    "IPR041577": "Reverse transcriptase/retrotransposon-derived protein, RNase H-like domain",
    "IPR042423": "PiggyBac transposable element-derived protein 5",
    "IPR042566": "L1 transposable element, C-terminal domain",
    "IPR043636": "L1 transposable element, RRM domain",
    "IPR044730": "H-like domain, plant type",
    "IPR045345": "Retroviral nucleocapsid Gag protein p24, C-terminal domain",
    "IPR045358": "Ty3 transposon capsid-like protein",
    "IPR046229": "Transposase for transposon Tn554-like",
    "IPR046835": "Retrotransposon hot spot protein, N-terminal",
    "IPR046836": "Retrotransposon hot spot protein,C-terminal",
    "IPR047629": "IS1182 transposase",
    "IPR047647": "ISAs1 transposase",
    "IPR047650": "Transposase IS110-like",
    "IPR047653": "Tn3-like transposase",
    "IPR047654": "IS1634 transposase",
    "IPR047655": "Transposase IS630-like",
    "IPR047656": "IS481-like transposase",
    "IPR047658": "IS4-like transposase",
    "IPR047661": "Insertion sequence IS21-like ATPase IstB",
    "IPR047768": "Transposase for transposon Tn5-like",
    "IPR047797": "ISNCY transposase",
    "IPR047883": "Regulator of Ty1 transposition protein 103-like, CID domain",
    "IPR047930": "IS6 family transposase",
    "IPR047951": "Transposase ISL3",
    "IPR047952": "IS4 family transposase",
    "IPR047959": "IS5 family transposase",
    "IPR047960": "IS1380 family transposase",
    "IPR048000": "Heteromeric transposase endonuclease subunit TnsA-like",
    "IPR048020": "IS3 transposase",
    "IPR048365": "Transposable element P transposase-like, RNase H domain, N-terminal",
    "IPR048366": "Transposable element P transposase-like, GTP-binding insertion domain",
    "IPR048367": "Transposable element P transposase-like, RNase H, C-terminal domain",
    "IPR048703": "Transposable element Tc3 transposase-like, DNA-binding HTH domain",
    "IPR049012": "Mutator-like transposase domain",
    "IPR049343": "Transposase protein",
    "IPR049837": "Transposon-encoded protein TnpC-like",
    "IPR050092": "Ribonuclease H",
    "IPR050195": "Primate lentivirus group Gag polyprotein-like",
    "IPR050462": "Retroviral Gag-Pol polyproteins",
    "IPR050900": "Transposase IS3/IS150/IS904",
    "IPR050917": "Transposase/Integrase Enzymes",
    "IPR051252": "IS1 element transposase InsA",
    "IPR051354": "Transposase 27 family, IS1 element",
    "IPR051399": "RNA-guided DNA endonucleases/Transposases",
    "IPR051698": "Transposase 11-like",
    "IPR051917": "Transposase/Integrase Enzymes",
    "IPR052160": "Gypsy Retrotransposon Integrase-like",
    "IPR052183": "Bacterial Insertion Sequence Transposase",
    "IPR052343": "Diverse Retrotransposon and Effector-Associated Protein",
    "IPR052344": "Transposase-related protein",
    "IPR052546": "Transposase_8_domain-containing_protein",
    "IPR052560": "RNA-directed DNA polymerase, mobile element",
    "IPR052638": "PiggyBac transposable element-derived",
    "IPR052715": "REP-associated tyrosine transposase",
    "IPR052909": "Transposase_6_like",
    "IPR053134": "RNA-directed DNA polymerase homolog",
    "IPR053164": "IS1016-like transposase",
    "IPR053172": "Tn903 transposase-like",
    "IPR053179": "LINE-1 ORF2p reverse transcriptase/endonuclease",
    "IPR053392": "Transposase IS30-like",
    "IPR053520": "Transposase_Tn903",
    "IPR053522": "RNA-guided DNA endonuclease TnpB-like",
    "IPR054353": "Transposase for insertion sequence element IS21-like, C-terminal domain",
    "IPR054832": "Transposase IS91 family",
    "IPR054836": "Transposase for transposon Tn5",
    "IPR055247": "Insertion element IS150 protein InsJ-like, helix-turn-helix domain"
}



    
    # Initialize counters and results list
    total_proteins = 0
    matched_proteins = []

    # Process the input file
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            total_proteins += 1
            protein_name = row[0]  # Protein name in the first column
            interpro_id = row[11]  # InterPro ID in the 12th column
            if interpro_id in transposon_interpro_ids:
                matched_proteins.append({
                    "protein": protein_name,
                    "interpro_id": interpro_id,
                    "description": transposon_interpro_ids[interpro_id]
                })

    # Write the report
    with open(output_file, 'w') as report:
        report.write("FPIdentifier Report\n")
        report.write("===================\n")
        report.write("Purpose:\n")
        report.write("FPIdentifier detects transposable proteins (False Positives) in the input protein sequences.\n\n")
        report.write(f"Input File: {input_file}\n")
        report.write(f"Total Proteins Analyzed: {total_proteins}\n\n")
        report.write("Results:\n")
        
        if matched_proteins:
            report.write("The following proteins were identified as transposable proteins:\n\n")
            for i, protein in enumerate(matched_proteins, 1):
                report.write(f"{i}. Protein: {protein['protein']}\n")
                report.write(f"   InterPro ID: {protein['interpro_id']}\n")
                report.write(f"   Description: {protein['description']}\n\n")
            report.write("Summary:\n")
            report.write(f"A total of {len(matched_proteins)} transposable proteins were detected.\n")
        else:
            report.write("No transposable proteins were detected in the input data.\n\n")
            report.write("Summary:\n")
            report.write("The analysis did not find any transposable proteins in the provided sequences.\n")
            report.write("Please review the input file to ensure accuracy or consider using alternative datasets.\n")

    print(f"Report generated successfully: {output_file}")
