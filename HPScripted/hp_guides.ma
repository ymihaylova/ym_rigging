//Maya ASCII 2019 scene
//Name: hp_guides.ma
//Last modified: Thu, Mar 25, 2021 07:33:50 PM
//Codeset: UTF-8
requires maya "2019";
requires "stereoCamera" "10.0";
requires "mtoa" "3.2.2";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "201907021615-48e59968a3";
fileInfo "osv" "Mac OS X 10.16";
createNode transform -s -n "persp";
	rename -uid "F5000D65-A74B-024C-315C-888950C3B9E9";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -51.112623152047455 158.78681113508375 27.88265492879005 ;
	setAttr ".r" -type "double3" -69.338352729798913 22.199999999998496 3.4352043726674711e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "D3ED0E91-414F-3D17-0731-888E304D9C58";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 70.498496834173011;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 67.184816067940375 93.320779581364263 -9.2663191025290388 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "FB5EFDE0-1E43-A4BF-A638-E5A303DABBDB";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -46.462214246900054 1002.4622990745301 -9.0604849529188467 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "03EC11CE-1149-A389-F91A-A7B2F6D77C85";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 909.1890396739102;
	setAttr ".ow" 47.894075795133489;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".tp" -type "double3" 68.213767981609635 93.273259400619665 -9.0853320815978087 ;
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "3392CACB-6149-9FD0-6C82-A296FCFF362C";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.3018118542918771 76.966156811369743 1012.8480248715941 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "D06FF1CC-9E41-CB1C-0E29-368A0FD979C1";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1021.8865915722455;
	setAttr ".ow" 95.488730970082898;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".tp" -type "double3" 61.84305208221916 93.422817469996858 -9.0385667006513799 ;
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "6C3F2F3E-7F43-F63D-D09B-DF87F2BC2E63";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 90.724510493534524 -8.6710355795991525 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "A583D25C-904B-45EB-533D-C2A1DC164C2D";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 12.037953721365577;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode joint -n "C_spine00_JNT";
	rename -uid "76D93855-264D-BA69-D8FD-6581DA631A0B";
	setAttr ".t" -type "double3" -1.4791141972893971e-31 71.231753005786189 -3.9471626995271571 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 89.999999999999986 ;
	setAttr ".radi" 0.85400402389735852;
createNode joint -n "C_spine01_JNT" -p "C_spine00_JNT";
	rename -uid "CE3F27D0-8D43-F3E1-D33F-72AEDDEB160D";
	setAttr ".t" -type "double3" 5.9869867981359448 1.1165194742223231e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode joint -n "C_spine02_JNT" -p "C_spine01_JNT";
	rename -uid "9F933804-D14A-E654-1EE7-73A36B8F4C66";
	setAttr ".t" -type "double3" 5.9869867981359448 1.2314553024510963e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode joint -n "C_spine03_JNT" -p "C_spine02_JNT";
	rename -uid "9528CEA3-3A44-9B7C-8865-BCAC29F43C47";
	setAttr ".t" -type "double3" 5.9869867981359448 1.0180030500262279e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode joint -n "C_spine04_JNT" -p "C_spine03_JNT";
	rename -uid "5409853F-6049-C0FD-47FD-07A362C167C0";
	setAttr ".t" -type "double3" 5.9869867981359448 6.896149693726185e-16 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode joint -n "L_leg00_JNT";
	rename -uid "CCD4B187-7E44-270B-3364-B8B9986886F1";
	setAttr ".t" -type "double3" 5.7680370343854452 71.23175048828125 -3.9471626281738281 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -1.0784501060306334e-13 0.51333926994008583 -89.999999999999986 ;
	setAttr ".radi" 2;
createNode joint -n "L_leg01_JNT" -p "L_leg00_JNT";
	rename -uid "681FF347-2442-F003-5E54-5CA19C9D9CF9";
	setAttr ".t" -type "double3" 32.385605920961183 -1.0256925994932212e-14 2.8090035437412429e-16 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 2.9024139014225163 0 ;
	setAttr ".radi" 2;
createNode joint -n "L_leg02_JNT" -p "L_leg01_JNT";
	rename -uid "F30F666A-6641-EE05-27CC-D6A9BC008D5F";
	setAttr ".t" -type "double3" 31.376458605828795 -3.1974423109204508e-14 -5.9507954119908391e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.415753171362601 -1.1370005665530335e-15 89.999999999999986 ;
	setAttr ".radi" 1.1855569000862318;
createNode joint -n "L_leg03_JNT" -p "L_leg02_JNT";
	rename -uid "D25706FD-6E4C-A489-1123-60901F485233";
	setAttr ".t" -type "double3" 0 -6.5245660050455347 10.834184064065022 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".jo" -type "double3" 9.9392333795734871e-15 -3.7900018885101651e-16 3.1794246203471362e-14 ;
	setAttr ".radi" 0.85377385509994741;
createNode joint -n "L_leg04_JNT" -p "L_leg03_JNT";
	rename -uid "F04DD4F7-5948-22A2-A13C-96A2EB6A7C13";
	setAttr ".t" -type "double3" 1.7598876477931024e-15 4.6949763359769114e-47 7.9258293548149528 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.85823255283525635;
createNode joint -n "L_arm00_JNT";
	rename -uid "D9C108AA-BB44-3577-668B-2E9291BA075D";
	setAttr ".t" -type "double3" 2.797356167909304 102.36337256441594 -4.7815617859206903 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 6.2383045022609265 18.988234985807932 18.570066859051014 ;
	setAttr ".radi" 1.0757147504503555;
createNode joint -n "L_arm01_JNT" -p "L_arm00_JNT";
	rename -uid "4E9FECD1-7A4C-FD6C-B9F0-AB826FC02D03";
	setAttr ".t" -type "double3" 9.0096668723278341 -3.7767098476360061e-15 1.4810201676151991e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 5.4603379164774415 -16.464823833644392 -33.69998077687854 ;
	setAttr ".radi" 2;
createNode joint -n "L_arm02_JNT" -p "L_arm01_JNT";
	rename -uid "3655D9FB-7E43-F1FE-71F4-EC873B40D42A";
	setAttr ".t" -type "double3" 19.89190691596583 -1.8610885443448017e-14 -2.5025059413245448e-15 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.00023988519189051374 -4.9248537980479767 0 ;
	setAttr ".radi" 2;
createNode joint -n "L_arm03_JNT" -p "L_arm02_JNT";
	rename -uid "3CA694F5-EE49-F558-6647-0496E0329D02";
	setAttr ".t" -type "double3" 20.610565543990514 -3.1997344035925118e-14 2.3081395227385615e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0.58361417877056088 2.1026299873189367 15.517274185770294 ;
	setAttr ".radi" 0.71995575926100663;
createNode joint -n "L_arm04_JNT" -p "L_arm03_JNT";
	rename -uid "8E583297-3149-9A9C-4628-D1B0B7C25760";
	setAttr ".t" -type "double3" 5.252478012379469 -5.5600672800524057e-15 -1.9174809426711426e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.71995575926100663;
createNode joint -n "R_arm00_JNT";
	rename -uid "D1621F57-E44A-48C4-59BA-F79A148AFD11";
	setAttr ".t" -type "double3" -2.79736 102.363 -4.78156 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -173.76169549773905 -18.988234985807939 -18.570066859051011 ;
	setAttr ".radi" 1.0757147504503555;
createNode joint -n "R_arm01_JNT" -p "R_arm00_JNT";
	rename -uid "B6B1CDDF-D542-AA48-F26A-5399A805B53A";
	setAttr ".t" -type "double3" -9.0096232757880941 0.00011864592791255291 7.2020348707013682e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 5.4603379164774424 -16.464823833644409 -33.699980776878512 ;
	setAttr ".radi" 2;
createNode joint -n "R_arm02_JNT" -p "R_arm01_JNT";
	rename -uid "EAF7A166-4149-FA63-CACF-92B22F0B36DE";
	setAttr ".t" -type "double3" -19.891796154763174 -0.00053309994977723818 7.312420015281873e-06 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.000239884567313887 -4.9248537980479963 1.0033825913442411e-14 ;
	setAttr ".radi" 2;
createNode joint -n "R_arm03_JNT" -p "R_arm02_JNT";
	rename -uid "A947AC10-024C-932A-CCE5-EEB1E7AB80FB";
	setAttr ".t" -type "double3" -20.610579830735436 5.78251133873664e-05 6.1526893553320861e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0.58361417816361139 2.102629987486039 15.517274185748196 ;
	setAttr ".radi" 0.71995575926100663;
createNode joint -n "R_arm04_JNT" -p "R_arm03_JNT";
	rename -uid "4D76E23C-724B-48CB-0CD3-008B15CA8BFC";
	setAttr ".t" -type "double3" -5.2524000237835153 -1.0778457109950068e-05 -6.5431660045689455e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159408e-07 3.003150310075944e-22 -6.5165243655873054e-23 ;
	setAttr ".radi" 0.71995575926100663;
createNode transform -n "C_spine_CRV";
	rename -uid "CE072CA3-3640-DAF6-123F-598A1849D4D3";
createNode nurbsCurve -n "C_spine_CRVShape" -p "C_spine_CRV";
	rename -uid "E0A6E1B5-0D48-DBE1-2BE3-35AF78596661";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 2 0 no 3
		7 0 0 0 11.97397359627189 23.947947192543779 23.947947192543779 23.947947192543779
		
		5
		-1.4791141972893971e-31 71.231753005786189 -3.9471626995271571
		-9.8607613152626476e-32 75.223077537876435 -3.947162699527158
		-8.0498805338025561e-17 83.20572660205849 -3.9471626995271594
		1.2619196770616295e-15 91.188375666239324 -3.9471626995271571
		1.2619196770616295e-15 95.179700198329968 -3.9471626995271571
		;
createNode joint -n "R_leg00_JNT";
	rename -uid "2257CFFE-8349-883A-CAC8-09AC4FB86940";
	setAttr ".t" -type "double3" -5.76804 71.2318 -3.94716 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -179.99999999999937 -0.51333926994008583 89.999999999999986 ;
	setAttr ".radi" 2;
createNode joint -n "R_leg01_JNT" -p "R_leg00_JNT";
	rename -uid "20FE84F5-2B42-33E7-065B-1BB5B9AE25BB";
	setAttr ".t" -type "double3" -32.385699871788653 1.1546319456101628e-14 5.485303003816e-06 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -6.3226718317248768e-16 2.9024139014223902 -2.4957497684415609e-14 ;
	setAttr ".radi" 2;
createNode joint -n "R_leg02_JNT" -p "R_leg01_JNT";
	rename -uid "28F38B83-1C4A-1805-F5CA-9F94CCA2D8CD";
	setAttr ".t" -type "double3" -31.376410530425424 2.5757174171303632e-14 -2.6520737277380135e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.4157531713624851 6.1702760820392226e-13 89.999999999999943 ;
	setAttr ".radi" 1.1855569000862318;
createNode joint -n "R_leg03_JNT" -p "R_leg02_JNT";
	rename -uid "D00BF868-F344-3EB4-9EE5-528945711905";
	setAttr ".t" -type "double3" 0 6.5245694508361876 -10.834182250976564 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.85377385509994741;
createNode joint -n "R_leg04_JNT" -p "R_leg03_JNT";
	rename -uid "D1AB6F36-EF40-7703-17B3-E4A0AE97BABB";
	setAttr ".t" -type "double3" -8.5265128291212022e-14 1.0269562977782698e-15 -7.92584 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "none";
	setAttr ".radi" 0.85823255283525635;
createNode transform -n "L_heel_LTR";
	rename -uid "266C7ED4-BB46-D964-CB69-60A951832DAB";
	setAttr ".t" -type "double3" 5.7680370343854266 -1.7763568394002505e-15 -10.462594570118583 ;
createNode locator -n "L_heel_LTRShape" -p "L_heel_LTR";
	rename -uid "2A817F41-DB40-D720-4D84-F3A4BE48E168";
	setAttr -k off ".v";
createNode transform -n "L_toes_LTR";
	rename -uid "18AC9DB1-BC4D-E9A3-C2BB-4AA1B37A5550";
	setAttr ".t" -type "double3" 5.7680370343854266 0.49912920569357139 11.346870609433896 ;
createNode locator -n "L_toes_LTRShape" -p "L_toes_LTR";
	rename -uid "AC3C9DBF-7140-88FF-B5E8-C1B57CD4AE1A";
	setAttr -k off ".v";
createNode transform -n "L_ballFoot_LTR";
	rename -uid "D8656886-344B-31CB-5E75-AC9FFAD61DBE";
	setAttr ".t" -type "double3" 5.7680370343854266 1.0021605491638184 4.7274322509765625 ;
createNode locator -n "L_ballFoot_LTRShape" -p "L_ballFoot_LTR";
	rename -uid "3C148E0C-7845-56CA-6A0A-2B9598E95EF9";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 5.09 5.09 5.09 ;
createNode transform -n "R_heel_LTR";
	rename -uid "8155BA62-B748-B25D-56EA-FFB38B389F37";
	setAttr ".t" -type "double3" -5.768 -2.6645352591003757e-15 -10.462594570118583 ;
	setAttr ".r" -type "double3" 180 0 0 ;
createNode locator -n "R_heel_LTRShape" -p "R_heel_LTR";
	rename -uid "B75FBF4C-B247-5FCA-2F18-209D6F5C01BD";
	setAttr -k off ".v";
createNode transform -n "R_toes_LTR";
	rename -uid "97701B05-C14B-A3BD-ED1B-87836AB6252F";
	setAttr ".t" -type "double3" -5.768 0.49912920569357144 11.346870609433896 ;
	setAttr ".r" -type "double3" 180 0 0 ;
createNode locator -n "R_toes_LTRShape" -p "R_toes_LTR";
	rename -uid "CCF6BEC2-724D-5BD3-DFA1-C8A38C5108CA";
	setAttr -k off ".v";
createNode transform -n "R_ballFoot_LTR";
	rename -uid "D714798C-5A48-B8B8-2B0E-97849A217340";
	setAttr ".t" -type "double3" -5.768 1.0021605491638181 4.7274322509765625 ;
	setAttr ".r" -type "double3" 180 0 0 ;
createNode locator -n "R_ballFoot_LTRShape" -p "R_ballFoot_LTR";
	rename -uid "869A5930-8246-C7C8-A5BB-7AA50C1288A9";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 5.09 5.09 5.09 ;
createNode joint -n "C_neck00_JNT";
	rename -uid "72CC8CF9-C346-2864-BF3B-EE847029DA9F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.010916553286908923 105.20215536928178 -7.2966374052915217 ;
	setAttr ".r" -type "double3" 1.180312431379028e-06 7.1562477364031365e-15 2.8823776874473675e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -2.4499373102423489e-15 -12.163428217328189 90.000000000000014 ;
	setAttr ".bps" -type "matrix" -2.6347468044113365e-16 0.97755058336477296 0.210700870817354 0
		 -0.99999999999999978 -2.2204460492503123e-16 -4.1799547317227625e-17 0 4.4614919397778507e-17 -0.21070087081735386 0.97755058336477318 0
		 0.010916553286908921 105.20215536928178 -7.2966374052915484 1;
	setAttr ".radi" 1.5;
	setAttr ".liw" yes;
createNode joint -n "C_neck01_JNT" -p "C_neck00_JNT";
	rename -uid "348C703B-724E-430B-3199-19B76C3282D0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.1724414825439453 -1.5080329693328842e-10 -2.9632994014150427e-07 ;
	setAttr ".jo" -type "double3" -2.6805825642663004e-15 0 -1.2436612337152885e-14 ;
	setAttr ".bps" -type "matrix" -2.6348823296828972e-16 0.97755058336477318 0.21070087081735372 0
		 -0.99999999999999978 -2.2204460492503126e-16 -4.1799547317227613e-17 0 4.4614919397778507e-17 -0.21070087081735386 0.97755058336477307 0
		 0.010916553437712221 114.16868095385884 -5.3639962870757989 1;
	setAttr ".radi" 1.5;
	setAttr ".liw" yes;
createNode joint -n "C_neck02_JNT" -p "C_neck01_JNT";
	rename -uid "EF820FC4-8B48-2702-20FA-B0BEBB295FE6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.1724414825439595 1.5080332989303447e-10 2.9632993658879059e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.6805825642663004e-15 0 -1.2436612337152885e-14 ;
	setAttr ".bps" -type "matrix" -4.15105899682058e-17 0.97755058336477307 0.210700870817354 0
		 -0.99999999999999989 0 -2.7921762818135717e-17 0 -3.8644802883681134e-17 -0.21070087081735395 0.97755058336477341 0
		 0.01091655328690813 123.13520641356195 -3.4313545895050575 1;
	setAttr ".radi" 1.5;
	setAttr ".liw" yes;
createNode joint -n "C_neckWithTwist00_JNT";
	rename -uid "C0B25B72-6645-6E22-770A-128593DECA3A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.010916553286908923 105.20215536928178 -7.2966374052915217 ;
	setAttr ".r" -type "double3" 1.180312431379028e-06 7.1562477364031365e-15 2.8823776874473675e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 -12.163428217328191 90 ;
	setAttr ".bps" -type "matrix" -2.6347468044113365e-16 0.97755058336477296 0.210700870817354 0
		 -0.99999999999999978 -2.2204460492503123e-16 -4.1799547317227625e-17 0 4.4614919397778507e-17 -0.21070087081735386 0.97755058336477318 0
		 0.010916553286908921 105.20215536928178 -7.2966374052915484 1;
	setAttr ".radi" 1.5;
	setAttr ".liw" yes;
createNode joint -n "C_neckWithTwist01_JNT" -p "C_neckWithTwist00_JNT";
	rename -uid "93D03E9D-4940-1C91-3011-60B9AD645525";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 18.344882965087905 3.4694469519536142e-17 -3.5527136788005009e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 8.8278125961003172e-32 ;
	setAttr ".bps" -type "matrix" -4.15105899682058e-17 0.97755058336477307 0.210700870817354 0
		 -0.99999999999999989 0 -2.7921762818135717e-17 0 -3.8644802883681134e-17 -0.21070087081735395 0.97755058336477341 0
		 0.01091655328690813 123.13520641356195 -3.4313545895050575 1;
	setAttr ".radi" 1.5;
	setAttr ".liw" yes;
createNode joint -n "L_index00_JNT";
	rename -uid "FF4707B6-554F-FC41-CDFE-92A727FF237C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 54.476448079200551 94.068634108523284 -5.0389455121634779 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -2.8281297996702355e-12 -7.9643318704675812 -1.6489004715497608 ;
	setAttr ".bps" -type "matrix" 0.98994456336698033 -0.028497989153691502 0.13855549817438406 0
		 0.028221943979104824 0.99959384980473132 0.0039569319680140339 0 -0.13861198843605105 -6.8377818738805337e-06 0.99034676584267645 0
		 54.476161524441267 94.068703717645846 -5.0389545490120513 1;
	setAttr ".radi" 0.68139072654771771;
	setAttr ".liw" yes;
createNode joint -n "L_index01_JNT" -p "L_index00_JNT";
	rename -uid "F5B09AF9-FD48-AB17-C8B5-19BE2FBEE4DD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.5282082538007566 -5.7675614804104482e-15 1.5144420481772689e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.4428279874127381 7.0081957964269561 -3.1972012790330124 ;
	setAttr ".bps" -type "matrix" 0.9994715239788039 -0.028281926491412531 0.016025148655086668 0
		 0.028419742442205687 0.99956045855923759 -0.0084384787943479825 1.7347234759768071e-18
		 -0.015779448501197064 0.0088894498580254933 0.99983597989181161 5.4210108624275222e-20
		 58.958836667080305 93.939658887912074 -4.4115463985438277 1;
	setAttr ".radi" 0.63332624188616926;
	setAttr ".liw" yes;
createNode joint -n "L_index02_JNT" -p "L_index01_JNT";
	rename -uid "3BD10442-CF41-D44C-B628-20ABEB43BA05";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.5825325315865029 -9.925054998299812e-16 -3.6973817597183581e-16 ;
	setAttr ".r" -type "double3" 3.222789143609152e-21 -9.9402343566282687e-16 6.4605016966775702e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 0 -1.2448989460169635 ;
	setAttr ".bps" -type "matrix" 0.99936602072052327 -0.031774757544292251 0.016059931887453156 0
		 0.031912309804821182 0.99945552148036887 -0.0083824259808231716 0 -0.015784838046339882 0.008889621218276425 0.99983589329571854 0
		 62.534586646236356 93.838476317287558 -4.3542141748689724 1;
	setAttr ".radi" 0.5923942728685555;
	setAttr ".liw" yes;
createNode joint -n "L_index03_JNT" -p "L_index02_JNT";
	rename -uid "B6C67319-6942-C783-FB03-B296D921C154";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.7765334409831777 1.7160661143471332e-14 3.2873856902707749e-16 ;
	setAttr ".r" -type "double3" -1.9132689772820423e-15 -1.5166066558319847e-21 -7.9513867036533695e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 0 -4.1579887545745828 ;
	setAttr ".bps" -type "matrix" 0.99708457333009826 -0.07452022203365806 0.016403967056471597 2.1684043449710089e-19
		 0.074653795499747266 0.99717989159890985 -0.007686000798185981 5.2041704279304213e-18
		 -0.015784943605132499 0.0088882112284925114 0.99983590416454793 -2.7105054312137611e-20
		 65.319109472027776 93.749942651111482 -4.3094665588863394 0.99999999999999967;
	setAttr ".radi" 0.56596025797259097;
	setAttr ".liw" yes;
createNode joint -n "L_index04_JNT" -p "L_index03_JNT";
	rename -uid "CA4C59CE-7B4E-E1FA-E98A-CAA5EE1B84E3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.2359605996918526 -7.9452242610834423e-15 -1.0168049922665309e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99708457333009815 -0.074520222033657699 0.01640396705647152 0
		 0.074653795499747266 0.99717989159890719 -0.0076860007981859393 0 -0.015784943605132523 0.008888211228492527 0.99983590416454915 0
		 67.536535228106132 93.584216428777367 -4.2729856223410545 1;
	setAttr ".radi" 0.56596025797259097;
	setAttr ".liw" yes;
createNode joint -n "L_thumb00_JNT";
	rename -uid "205697B2-7F45-4F40-B7C3-66BA6EB79710";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 51.050859263607904 93.116241371059402 -5.1905099038486142 ;
	setAttr ".r" -type "double3" -7.9513867036587939e-16 -5.5659706925611528e-15 6.361109362927032e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 11.105095491345761 -39.833848700437521 -17.03636548119346 ;
	setAttr ".bps" -type "matrix" 0.83162268209109114 -0.27471250801937891 0.4826352168763916 4.3368086899420177e-19
		 -0.42919989734932895 0.23355932559393683 0.87248924895578528 -4.3368086899420177e-19
		 -0.35240766556212266 -0.93272883485276881 0.07632665253532217 1.7347234759768071e-18
		 51.912868756745063 92.891607255246782 -3.955151642190875 0.99999999999999989;
	setAttr ".radi" 0.55113468018023726;
	setAttr ".liw" yes;
createNode joint -n "L_thumb01_JNT" -p "L_thumb00_JNT";
	rename -uid "9F7B9281-184E-DC19-6BDF-34AC919C3C8D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.4269024761176232 -4.0336638628122933e-15 1.2629240643653995e-15 ;
	setAttr ".r" -type "double3" -1.4672793276595362e-14 7.8085102238274209e-15 -5.7274832349792229e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 69.877605408221427 11.313106524437057 -7.688975553281221 ;
	setAttr ".bps" -type "matrix" 0.82019488031557208 -0.34646030251808163 0.45524237180122457 2.1250362580715887e-17
		 -0.38385623910660183 0.25675073686273148 0.88697995852182465 -5.6378512969246231e-18
		 -0.42418715916805178 -0.90224404564370708 0.07759469116773475 1.0408340855860843e-17
		 53.566636796493057 92.345312913237265 -2.9953814077819669 0.999999999999998;
	setAttr ".radi" 0.6512726984488395;
	setAttr ".liw" yes;
createNode joint -n "L_thumb02_JNT" -p "L_thumb01_JNT";
	rename -uid "946E1912-4E4F-D6B6-3BE1-0781C4662645";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.9246055033440896 -7.6605388699135801e-15 -1.4210854715202004e-14 ;
	setAttr ".r" -type "double3" 8.4172882683263017e-15 6.5800830983207633e-15 8.0236014461822589e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.53329646848106638 1.38962738613046 -2.4087600009620642 ;
	setAttr ".bps" -type "matrix" 0.8456443286178994 -0.33495952543946145 0.41555719918412359 0
		 -0.35278887222936639 0.23347635175579209 0.90610639816852345 0 -0.40053174793955348 -0.91284769238256613 0.079267959506410759 0
		 56.785578137594257 90.985592903284569 -1.2087346900554592 1;
	setAttr ".radi" 0.57494026552459554;
	setAttr ".liw" yes;
createNode joint -n "L_thumb03_JNT" -p "L_thumb02_JNT";
	rename -uid "D167822F-984A-48E1-F9D0-B58FCF8B4F0C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.5969999999999978 2.7616797737550769e-15 -7.1054273576010019e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.9513867036587919e-16 -1.1927080055488188e-15 3.1805546814635168e-15 ;
	setAttr ".bps" -type "matrix" 0.84564432861789784 -0.33495952543946211 0.41555719918412365 -4.7704895589362195e-18
		 -0.35278887222936717 0.23347635175579204 0.90610639816852512 -1.3010426069826053e-18
		 -0.40053174793955315 -0.9128476923825658 0.079267959506410773 0 58.981716459014933 90.115703015718395 -0.1295326437742885 0.99999999999999944;
	setAttr ".radi" 0.57494026552459554;
	setAttr ".liw" yes;
createNode joint -n "L_ring00_JNT";
	rename -uid "1B24603F-314B-869B-B351-5C8046C8368A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 54.676619257505884 93.906273137968526 -9.2333369775353393 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -3.1012322720947153e-12 -0.20897279347935072 4.8096714828080014 ;
	setAttr ".bps" -type "matrix" 0.99647208007290478 0.083845653799268588 0.00364691296210423 0
		 -0.083845117543174807 0.99647875355756499 -0.00029995421383909038 0 -0.0036592211399794875 -6.8798465863741209e-06 0.99999330500424555 0
		 54.676328868338423 93.906371597022584 -9.2333473140281139 1;
	setAttr ".radi" 0.66930120983950681;
	setAttr ".liw" yes;
createNode joint -n "L_ring01_JNT" -p "L_ring00_JNT";
	rename -uid "38EC62F0-F347-0308-7348-4981CCD5B9B0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.3036749230357012 3.1768838206427147e-15 1.2691666067336438e-16 ;
	setAttr ".r" -type "double3" 4.9376161476373356e-10 -1.0582829011152106e-10 -1.0050584763569866e-11 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 0 -9.7381252132524114 ;
	setAttr ".bps" -type "matrix" 0.99620141923419503 -0.085910569722443306 0.014216410437793616 1.0842021724855044e-19
		 0.085901724636801458 0.99630285253160722 0.0012327780852755821 -1.7347234759768071e-18
		 -0.014269758939580914 -6.881103401307467e-06 0.99989818178275325 1.3234889800848443e-23
		 58.964820770852491 94.267216034693163 -9.2176521861390306 0.99999999999999989;
	setAttr ".radi" 0.6481660280284246;
	setAttr ".liw" yes;
createNode joint -n "L_ring02_JNT" -p "L_ring01_JNT";
	rename -uid "A7BB3BDD-7548-1276-9A50-669442F7A29C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.8625290994323151 1.9906984551925274e-14 -2.0771301706829402e-16 ;
	setAttr ".r" -type "double3" 0 0 -1.0044191684061787e-11 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 0 -1.4342352251493724 ;
	setAttr ".bps" -type "matrix" 0.9840113505996243 -0.17755137111935043 0.014041812729863719 0
		 0.17753319653210636 0.98411153360088732 0.0025403863491167966 0 -0.01426975893958092 -6.8811034013192162e-06 0.99989818178275391 0
		 62.812677741540178 93.935383959190858 -9.1627408871264659 1;
	setAttr ".radi" 0.60123688873639081;
	setAttr ".liw" yes;
createNode joint -n "L_ring03_JNT" -p "L_ring02_JNT";
	rename -uid "148AE56C-8847-D1CA-F2A0-399AEABC7B53";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.869630503284029 3.9447544081076813e-15 3.9829251008427491e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 0 -1.3609380807978213 ;
	setAttr ".bps" -type "matrix" 0.99638008326720096 -0.068911233511341749 0.049779228242201275 0
		 0.065986190028165859 0.99612231027547316 0.058190769861039049 0 -0.053596197570450102 -0.054695382505279291 0.99706362020614769 0
		 65.732759015790506 93.408495286913066 -9.1210714141198164 1;
	setAttr ".radi" 0.57555379215795255;
	setAttr ".liw" yes;
createNode joint -n "L_ring04_JNT" -p "L_ring03_JNT";
	rename -uid "C920D6AA-D34A-DC4E-C64F-82AC4DFD37D9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.6450691024815645 -6.6316648895427266e-15 2.8171909249863347e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99638008326719973 -0.068911233511342929 0.049779228242200949 0
		 0.065986190028165082 0.9961223102754726 0.05819076986103916 0 -0.053596197570450012 -0.054695382505279236 0.99706362020614669 0
		 68.200005665343056 93.237856579002354 -8.9978075751928106 1;
	setAttr ".radi" 0.57555379215795255;
	setAttr ".liw" yes;
createNode joint -n "L_midFinger00_JNT";
	rename -uid "FF4B5EEB-1F4A-14DC-E4F0-D7B82DD9EF8C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 54.655920809626636 94.507410131930797 -7.3054348849805031 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.25968692302658902 -5.2906966417368517 2.8140490709580455 ;
	setAttr ".bps" -type "matrix" 0.99453902606231048 0.048885072685394937 0.092208325587093867 3.3610267347050637e-18
		 -0.048676944142539647 0.99880441009308341 -0.0045061610655841994 0 -0.092318366254911369 -6.8664766338914493e-06 0.99572954119322843 -2.1590075732124065e-19
		 54.655632083999549 94.50749534383975 -7.3054410730863051 0.99999999999999989;
	setAttr ".radi" 0.69065892993629929;
	setAttr ".liw" yes;
createNode joint -n "L_midFinger01_JNT" -p "L_midFinger00_JNT";
	rename -uid "8DCBB314-4A40-1B0E-AE95-2791B8A0FB71";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.6916820776047814 1.4210854715202004e-14 1.4210854715202004e-14 ;
	setAttr ".r" -type "double3" 4.9597152254940719e-10 -9.5190473188323168e-11 -6.9668807897405883e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 4.8178826974307389 -8.9818635011602908 ;
	setAttr ".bps" -type "matrix" 0.99419927262689822 -0.10726858506491163 0.0078266829703794328 0
		 0.1072652068144111 0.99423007931304752 0.00085134965211698665 0 -0.0078728467029763015 -6.8804373971767532e-06 0.99996900863849192 0
		 59.321693008054602 94.736848563220363 -6.8728289245233762 1;
	setAttr ".radi" 0.65127017417596755;
	setAttr ".liw" yes;
createNode joint -n "L_midFinger02_JNT" -p "L_midFinger01_JNT";
	rename -uid "09960DB6-9742-7302-ED91-03B547446B65";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.947332549677661 5.6843418860808015e-14 -1.3322676295501878e-14 ;
	setAttr ".r" -type "double3" 0 0 -6.9638244750643701e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -4.9696166897867449e-17 -2.1290630885825985 ;
	setAttr ".bps" -type "matrix" 0.98952798696497435 -0.14413078899614265 0.0077896518787269609 4.3368086899420177e-19
		 0.14412626859054412 0.98955864688052031 0.0011415279923128741 1.7347234759768071e-18
		 -0.0078728467029763015 -6.8804373971705918e-06 0.99996900863849281 2.6469779601696886e-23
		 63.246128157760651 94.313423785835823 -6.8419344040784029 0.99999999999999967;
	setAttr ".radi" 0.61450227179012873;
	setAttr ".liw" yes;
createNode joint -n "L_midFinger03_JNT" -p "L_midFinger02_JNT";
	rename -uid "636F42F8-0B48-AD0C-4561-8989DF5C446C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.2476181047560644 -4.2632564145606011e-14 -2.9309887850104133e-14 ;
	setAttr ".r" -type "double3" 0 0 -6.9566682270310768e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.4848083448933731e-17 0 -4.0307459437827795 ;
	setAttr ".bps" -type "matrix" 0.97694947265358456 -0.21333211096315313 0.007690143944552307 0
		 0.21332544659902614 0.97697973898370138 0.0016862528461221299 0 -0.0078728467029763084 -6.8804373971699989e-06 0.99996900863849258 0
		 66.459737163390997 93.84534202603902 -6.8166365896073398 1;
	setAttr ".radi" 0.57933899281065215;
	setAttr ".liw" yes;
createNode joint -n "L_midFinger04_JNT" -p "L_midFinger03_JNT";
	rename -uid "23FECAA8-8442-2B8B-B36B-91BE37CC4CA3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.7877149148414966 6.0478710903086453e-14 -2.0122792321330962e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -4.9696166897867449e-17 -1.5014648549670148e-15 ;
	setAttr ".bps" -type "matrix" 0.97694947265358445 -0.21333211096315205 0.0076901439445522853 0
		 0.21332544659902597 0.97697973898370094 0.0016862528461221438 0 -0.0078728467029763136 -6.8804373971814313e-06 0.99996900863849303 0
		 68.836802925740216 93.326272748482069 -6.7979253067930241 1;
	setAttr ".radi" 0.57933899281065215;
	setAttr ".liw" yes;
createNode joint -n "L_pinky00_JNT";
	rename -uid "65807DB8-5E47-0ECD-F987-02848345DB84";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 54.640376606465928 93.766110953861428 -11.203357138790885 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -1.3506787127208867e-11 4.3983581544585189 -0.81686097833185178 ;
	setAttr ".bps" -type "matrix" 0.99983597708923799 -0.014244803417142312 -0.011185012007837569 5.4210108624275222e-20
		 0.014243989096213383 0.99989853761684988 -0.00015246740719870866 5.2041704279304213e-18
		 0.011186049018107014 -6.8767900297812016e-06 0.99993743417279468 -2.7078584532535914e-20
		 54.638483966584012 93.766223922580792 -11.346436045255002 0.99999999999999967;
	setAttr ".radi" 0.64155184490655581;
	setAttr ".liw" yes;
createNode joint -n "L_pinky01_JNT" -p "L_pinky00_JNT";
	rename -uid "FB5B3F70-384E-5656-6DA5-BD87E52A4D4C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.7476661451303594 -1.0041880521560742e-15 2.7755575615628914e-16 ;
	setAttr ".r" -type "double3" 4.9774476254058422e-10 -8.554406049520288e-11 5.6029326288368798e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0.49475199561393202 -2.9500150483946084 -6.4629190510637811 ;
	setAttr ".bps" -type "matrix" 0.99179361405910993 -0.12656974749284319 -0.018042342729345996 2.1684043449710089e-19
		 0.12654893553804997 0.99195771027415103 -0.0022951997411266856 -1.7347234759768071e-18
		 0.018187743833463936 -6.874820771912312e-06 0.99983458928313995 1.3234889800848443e-23
		 58.377480361268745 93.712953916459583 -11.388263625508271 0.99999999999999989;
	setAttr ".radi" 0.60562295843487834;
	setAttr ".liw" yes;
createNode joint -n "L_pinky02_JNT" -p "L_pinky01_JNT";
	rename -uid "5EA66618-874E-4D69-F94D-3EB2CF59C54A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.0446275124583702 -3.9273190819213988e-16 -5.2735593669694936e-16 ;
	setAttr ".r" -type "double3" 0 0 5.6003604400544788e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 0 0.83626176669921282 ;
	setAttr ".bps" -type "matrix" 0.99353419573159563 -0.11208539533488622 -0.01807390562644301 -3.2526065174565133e-18
		 0.11206697946415733 0.99369857809365891 -0.0020317500882971185 5.2041704279304213e-18
		 0.018187743833463992 -6.8748207718554057e-06 0.99983458928314084 1.3234889800848443e-23
		 61.396839273134454 93.327632323692995 -11.44319068648001 0.99999999999999978;
	setAttr ".radi" 0.56564578290185841;
	setAttr ".liw" yes;
createNode joint -n "L_pinky03_JNT" -p "L_pinky02_JNT";
	rename -uid "AC4BCE6B-9F4E-63A7-55BF-4CAC94600590";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.269236342342007 -2.6735670020103589e-14 1.3565537582138631e-15 ;
	setAttr ".r" -type "double3" 0 0 5.5998013581768779e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 0 0.11136891195885326 ;
	setAttr ".bps" -type "matrix" 0.99375029276816484 -0.11015238503007661 -0.018077823302913382 0
		 0.11013428892689825 0.99391471063915759 -0.0019965915064172196 0 0.018187743833463946 -6.874820771898917e-06 0.99983458928313906 0
		 63.651319184491655 93.07329354680472 -11.484203122015321 1;
	setAttr ".radi" 0.54911436848391437;
	setAttr ".liw" yes;
createNode joint -n "L_pinky04_JNT" -p "L_pinky03_JNT";
	rename -uid "2A1ECE4E-704E-D93E-C537-77BB384280C4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0646864332227719 6.1077323212054002e-14 -4.0838860071445993e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99375029276816496 -0.11015238503007556 -0.018077823302913559 0
		 0.11013428892689792 0.99391471063915893 -0.0019965915064172335 0 0.018187743833463946 -6.874820771908314e-06 0.99983458928313906 0
		 65.600499112351741 92.857236435205223 -11.519661657804262 1;
	setAttr ".radi" 0.54911436848391437;
	setAttr ".liw" yes;
createNode transform -n "L_footBankIn_LTR";
	rename -uid "53302653-1A43-B26B-CB84-6AA4DC52E6A3";
	setAttr ".t" -type "double3" 1.8277697563171387 -0.20600157976150513 5.0197787284851074 ;
createNode locator -n "L_footBankIn_LTRShape" -p "L_footBankIn_LTR";
	rename -uid "A167FE0D-DF47-5CCE-38D6-C6BE082D7CA7";
	setAttr -k off ".v";
createNode transform -n "L_footBankOut_LTR";
	rename -uid "E834C60E-E84D-8967-96F7-5681211890EC";
	setAttr ".t" -type "double3" 11.203033447265625 -0.20389336347579956 4.5645976066589355 ;
createNode locator -n "L_footBankOut_LTRShape" -p "L_footBankOut_LTR";
	rename -uid "82B0EB36-464C-A421-03A9-9A929B7B1E29";
	setAttr -k off ".v";
createNode transform -n "R_footBankOut_LTR";
	rename -uid "597211F3-5D48-871D-FD34-FCAC46CA4FB7";
	setAttr ".t" -type "double3" -11.203033447265625 -0.20389336347579956 4.5645976066589355 ;
	setAttr ".r" -type "double3" 180 0 0 ;
createNode locator -n "R_footBankOut_LTRShape" -p "R_footBankOut_LTR";
	rename -uid "54316875-BE46-A480-BA18-78ADB756233F";
	setAttr -k off ".v";
createNode transform -n "R_footBankIn_LTR";
	rename -uid "51848BB3-E243-F29E-44C3-1FBDD34B7559";
	setAttr ".t" -type "double3" -1.8277697563171387 -0.20600157976150513 5.0197787284851074 ;
	setAttr ".r" -type "double3" 180 0 0 ;
createNode locator -n "R_footBankIn_LTRShape" -p "R_footBankIn_LTR";
	rename -uid "A45260C2-CF45-29BB-985B-C1AC7C2999A0";
	setAttr -k off ".v";
createNode transform -n "back";
	rename -uid "C658B168-3246-E9CF-EAB8-6F9C247E8C47";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 65.701996619903781 92.845735087201859 -1006.7783354710726 ;
	setAttr ".r" -type "double3" 0 180 0 ;
createNode camera -n "backShape" -p "back";
	rename -uid "AA162731-FE40-2A4C-DE85-31A6537F291F";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".coi" 995.12451996731431;
	setAttr ".ow" 27.56406716475999;
	setAttr ".imn" -type "string" "back1";
	setAttr ".den" -type "string" "back1_depth";
	setAttr ".man" -type "string" "back1_mask";
	setAttr ".tp" -type "double3" 65.701996619903653 92.845735087201859 -11.653815503758352 ;
	setAttr ".hc" -type "string" "viewSet -b %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode joint -n "R_index00_JNT";
	rename -uid "B66EE085-8343-0F11-8A87-F892ABDE17A2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -54.4764 94.0686 -5.03895 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 179.99999999999719 7.9643318704675909 1.6489004715497619 ;
	setAttr ".bps" -type "matrix" 0.98994456336698033 -0.028497989153691502 0.13855549817438406 0
		 0.028221943979104824 0.99959384980473132 0.0039569319680140339 0 -0.13861198843605105 -6.8377818738805337e-06 0.99034676584267645 0
		 54.476161524441267 94.068703717645846 -5.0389545490120513 1;
	setAttr ".radi" 0.68139072654771771;
	setAttr ".liw" yes;
createNode joint -n "R_index01_JNT" -p "R_index00_JNT";
	rename -uid "30BE5BA5-4640-06E4-7B2A-33BB7C90E4FE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.5282332255105757 -4.2077402881091075e-05 -3.4054131710092861e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.44282798740534085 7.0081957964270742 -3.1972012790326438 ;
	setAttr ".bps" -type "matrix" 0.9994715239788039 -0.028281926491412531 0.016025148655086668 0
		 0.028419742442205687 0.99956045855923759 -0.0084384787943479825 1.7347234759768071e-18
		 -0.015779448501197064 0.0088894498580254933 0.99983597989181161 5.4210108624275222e-20
		 58.958836667080305 93.939658887912074 -4.4115463985438277 1;
	setAttr ".radi" 0.63332624188616926;
	setAttr ".liw" yes;
createNode joint -n "R_index02_JNT" -p "R_index01_JNT";
	rename -uid "7BDCB3FC-B04E-F502-0D45-9AB716907E86";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.5825716988779277 4.9705110114928175e-05 5.3266307435961835e-06 ;
	setAttr ".r" -type "double3" 3.222789143609152e-21 -9.9402343566282687e-16 6.4605016966775702e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 5.6582578197798277e-16 -5.2081582908949627e-14 -1.2448989460166155 ;
	setAttr ".bps" -type "matrix" 0.99936602072052327 -0.031774757544292251 0.016059931887453156 0
		 0.031912309804821182 0.99945552148036887 -0.0083824259808231716 0 -0.015784838046339882 0.008889621218276425 0.99983589329571854 0
		 62.534586646236356 93.838476317287558 -4.3542141748689724 1;
	setAttr ".radi" 0.5923942728685555;
	setAttr ".liw" yes;
createNode joint -n "R_index03_JNT" -p "R_index02_JNT";
	rename -uid "52FAACF5-3340-F02B-5961-FA95482280A2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.7765242931690608 -4.8276275222747245e-05 -3.3868234323719548e-06 ;
	setAttr ".r" -type "double3" -1.9132689772820423e-15 -1.5166066558319847e-21 -7.9513867036533695e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 8.5377366010655943e-07 -3.8166656153272795e-13 -4.1579887545749719 ;
	setAttr ".bps" -type "matrix" 0.99708457333009826 -0.07452022203365806 0.016403967056471597 2.1684043449710089e-19
		 0.074653795499747266 0.99717989159890985 -0.007686000798185981 5.2041704279304213e-18
		 -0.015784943605132499 0.0088882112284925114 0.99983590416454793 -2.7105054312137611e-20
		 65.319109472027776 93.749942651111482 -4.3094665588863394 0.99999999999999967;
	setAttr ".radi" 0.56596025797259097;
	setAttr ".liw" yes;
createNode joint -n "R_index04_JNT" -p "R_index03_JNT";
	rename -uid "83B1106A-8F4D-9D04-0EAE-D491CAC2B526";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2359146470509117 -6.6400529874499625e-07 -1.6493324395128184e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99708457333009815 -0.074520222033657699 0.01640396705647152 0
		 0.074653795499747266 0.99717989159890719 -0.0076860007981859393 0 -0.015784943605132523 0.008888211228492527 0.99983590416454915 0
		 67.536535228106132 93.584216428777367 -4.2729856223410545 1;
	setAttr ".radi" 0.56596025797259097;
	setAttr ".liw" yes;
createNode joint -n "R_thumb00_JNT";
	rename -uid "FF924455-C745-6D69-0E4A-448CFFAAE60A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -51.0509 93.1162 -5.19051 ;
	setAttr ".r" -type "double3" -7.9513867036587939e-16 -5.5659706925611528e-15 6.361109362927032e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -168.89490450865418 39.833848700437528 17.036365481193471 ;
	setAttr ".bps" -type "matrix" 0.83162268209109114 -0.27471250801937891 0.4826352168763916 4.3368086899420177e-19
		 -0.42919989734932895 0.23355932559393683 0.87248924895578528 -4.3368086899420177e-19
		 -0.35240766556212266 -0.93272883485276881 0.07632665253532217 1.7347234759768071e-18
		 51.912868756745063 92.891607255246782 -3.955151642190875 0.99999999999999989;
	setAttr ".radi" 0.55113468018023726;
	setAttr ".liw" yes;
createNode joint -n "R_thumb01_JNT" -p "R_thumb00_JNT";
	rename -uid "1F4C7D90-A447-7156-BABE-B7A8C231F511";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.4268391158107949 -7.1434796069524964e-05 -4.1786841244118023e-05 ;
	setAttr ".r" -type "double3" -1.4672793276595362e-14 7.8085102238274209e-15 -5.7274832349792229e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 69.877605408221385 11.31310652443705 -7.6889755532812307 ;
	setAttr ".bps" -type "matrix" 0.82019488031557208 -0.34646030251808163 0.45524237180122457 2.1250362580715887e-17
		 -0.38385623910660183 0.25675073686273148 0.88697995852182465 -5.6378512969246231e-18
		 -0.42418715916805178 -0.90224404564370708 0.07759469116773475 1.0408340855860843e-17
		 53.566636796493057 92.345312913237265 -2.9953814077819669 0.999999999999998;
	setAttr ".radi" 0.6512726984488395;
	setAttr ".liw" yes;
createNode joint -n "R_thumb02_JNT" -p "R_thumb01_JNT";
	rename -uid "9A1EAB0F-CE4E-0D81-7601-EBB9849266D9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.924687374840591 4.5914862014551083e-05 -5.7084837919774145e-05 ;
	setAttr ".r" -type "double3" 8.4172882683263017e-15 6.5800830983207633e-15 8.0236014461822589e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.53329646848364942 1.3896273861304607 -2.4087600009620749 ;
	setAttr ".bps" -type "matrix" 0.8456443286178994 -0.33495952543946145 0.41555719918412359 0
		 -0.35278887222936639 0.23347635175579209 0.90610639816852345 0 -0.40053174793955348 -0.91284769238256613 0.079267959506410759 0
		 56.785578137594257 90.985592903284569 -1.2087346900554592 1;
	setAttr ".radi" 0.57494026552459554;
	setAttr ".liw" yes;
createNode joint -n "R_thumb03_JNT" -p "R_thumb02_JNT";
	rename -uid "ECC9A74F-2148-94A1-98C6-4E83B5D339B5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.5969399593778419 -3.0610230384531256e-05 6.0939873208099016e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.84564432861789784 -0.33495952543946211 0.41555719918412365 -4.7704895589362195e-18
		 -0.35278887222936717 0.23347635175579204 0.90610639816852512 -1.3010426069826053e-18
		 -0.40053174793955315 -0.9128476923825658 0.079267959506410773 0 58.981716459014933 90.115703015718395 -0.1295326437742885 0.99999999999999944;
	setAttr ".radi" 0.57494026552459554;
	setAttr ".liw" yes;
createNode joint -n "R_ring00_JNT";
	rename -uid "0799F167-E04F-4C73-B094-C5A1A1DBEBD7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -54.6766 93.9063 -9.23334 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 179.99999999995538 0.20897279347935407 -4.8096714828080742 ;
	setAttr ".bps" -type "matrix" 0.99647208007290478 0.083845653799268588 0.00364691296210423 0
		 -0.083845117543174807 0.99647875355756499 -0.00029995421383909038 0 -0.0036592211399794875 -6.8798465863741209e-06 0.99999330500424555 0
		 54.676328868338423 93.906371597022584 -9.2333473140281139 1;
	setAttr ".radi" 0.66930120983950681;
	setAttr ".liw" yes;
createNode joint -n "R_ring01_JNT" -p "R_ring00_JNT";
	rename -uid "2134DC4D-2B44-EC63-A0FC-78AAA3406B85";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.3036792838255948 4.4260376668603385e-05 -3.3833452892650939e-06 ;
	setAttr ".r" -type "double3" 4.9376161476373356e-10 -1.0582829011152106e-10 -1.0050584763569866e-11 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 1.4787786900419693e-06 7.5531961662000568e-12 -9.7381252132524718 ;
	setAttr ".bps" -type "matrix" 0.99620141923419503 -0.085910569722443306 0.014216410437793616 1.0842021724855044e-19
		 0.085901724636801458 0.99630285253160722 0.0012327780852755821 -1.7347234759768071e-18
		 -0.014269758939580914 -6.881103401307467e-06 0.99989818178275325 1.3234889800848443e-23
		 58.964820770852491 94.267216034693163 -9.2176521861390306 0.99999999999999989;
	setAttr ".radi" 0.6481660280284246;
	setAttr ".liw" yes;
createNode joint -n "R_ring02_JNT" -p "R_ring01_JNT";
	rename -uid "9B350C63-554E-F53A-AC30-8E8662DEB57B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.8625027033064185 -3.6464295902760568e-05 4.5702793389779117e-06 ;
	setAttr ".r" -type "double3" 0 0 -1.0044191684061787e-11 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 1.9095590847501325e-06 -3.7004458239151672e-08 -1.4342352251490609 ;
	setAttr ".bps" -type "matrix" 0.9840113505996243 -0.17755137111935043 0.014041812729863719 0
		 0.17753319653210636 0.98411153360088732 0.0025403863491167966 0 -0.01426975893958092 -6.8811034013192162e-06 0.99989818178275391 0
		 62.812677741540178 93.935383959190858 -9.1627408871264659 1;
	setAttr ".radi" 0.60123688873639081;
	setAttr ".liw" yes;
createNode joint -n "R_ring03_JNT" -p "R_ring02_JNT";
	rename -uid "0CB590D0-FF47-6545-AEB6-DEAA527E1504";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.8696922260437319 -2.6092789340736999e-05 -1.8368703358362382e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 3.5215939597884662e-06 -1.1745708907383513e-07 -1.3609380807979077 ;
	setAttr ".bps" -type "matrix" 0.99638008326720096 -0.068911233511341749 0.049779228242201275 0
		 0.065986190028165859 0.99612231027547316 0.058190769861039049 0 -0.053596197570450102 -0.054695382505279291 0.99706362020614769 0
		 65.732759015790506 93.408495286913066 -9.1210714141198164 1;
	setAttr ".radi" 0.57555379215795255;
	setAttr ".liw" yes;
createNode joint -n "R_ring04_JNT" -p "R_ring03_JNT";
	rename -uid "9814F75D-EB47-57B4-FAF6-C18A97183293";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.6450160653377708 2.2289296751409893e-05 -2.8631133162093647e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.0403978477281018e-06 -2.732657173654609e-20 1.4432906640220227e-14 ;
	setAttr ".bps" -type "matrix" 0.99638008326719973 -0.068911233511342929 0.049779228242200949 0
		 0.065986190028165082 0.9961223102754726 0.05819076986103916 0 -0.053596197570450012 -0.054695382505279236 0.99706362020614669 0
		 68.200005665343056 93.237856579002354 -8.9978075751928106 1;
	setAttr ".radi" 0.57555379215795255;
	setAttr ".liw" yes;
createNode joint -n "R_midFinger00_JNT";
	rename -uid "DBA5A9C4-824F-F065-D623-52971CFB710A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -54.6559 94.5074 -7.30543 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.74031307697717 5.2906966417368961 -2.8140490709580677 ;
	setAttr ".bps" -type "matrix" 0.99453902606231048 0.048885072685394937 0.092208325587093867 3.3610267347050637e-18
		 -0.048676944142539647 0.99880441009308341 -0.0045061610655841994 0 -0.092318366254911369 -6.8664766338914493e-06 0.99572954119322843 -2.1590075732124065e-19
		 54.655632083999549 94.50749534383975 -7.3054410730863051 0.99999999999999989;
	setAttr ".radi" 0.69065892993629929;
	setAttr ".liw" yes;
createNode joint -n "R_midFinger01_JNT" -p "R_midFinger00_JNT";
	rename -uid "1FC07042-BB48-FFB2-85C8-8E88C297E74A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.6917230289310226 -4.2734543413303072e-05 8.4920706928670597e-06 ;
	setAttr ".r" -type "double3" 4.9597152254940719e-10 -9.5190473188323168e-11 -6.9668807897405883e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.1813093300402509e-12 4.8178826974301838 -8.9818635011605998 ;
	setAttr ".bps" -type "matrix" 0.99419927262689822 -0.10726858506491163 0.0078266829703794328 0
		 0.1072652068144111 0.99423007931304752 0.00085134965211698665 0 -0.0078728467029763015 -6.8804373971767532e-06 0.99996900863849192 0
		 59.321693008054602 94.736848563220363 -6.8728289245233762 1;
	setAttr ".radi" 0.65127017417596755;
	setAttr ".liw" yes;
createNode joint -n "R_midFinger02_JNT" -p "R_midFinger01_JNT";
	rename -uid "0A6CED72-5544-CFE1-37B3-9084E6F55F23";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.9473057157903568 7.8030094499581537e-05 5.9680575148490789e-08 ;
	setAttr ".r" -type "double3" 0 0 -6.9638244750643701e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.3640068871139521e-15 -1.2722218725852679e-13 -2.1290630885823902 ;
	setAttr ".bps" -type "matrix" 0.98952798696497435 -0.14413078899614265 0.0077896518787269609 4.3368086899420177e-19
		 0.14412626859054412 0.98955864688052031 0.0011415279923128741 1.7347234759768071e-18
		 -0.0078728467029763015 -6.8804373971705918e-06 0.99996900863849281 2.6469779601696886e-23
		 63.246128157760651 94.313423785835823 -6.8419344040784029 0.99999999999999967;
	setAttr ".radi" 0.61450227179012873;
	setAttr ".liw" yes;
createNode joint -n "R_midFinger03_JNT" -p "R_midFinger02_JNT";
	rename -uid "E7D5DCEA-A040-900F-9432-3FBE8F7D9345";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.2475891178902785 -7.3849419521820892e-05 -2.607258995368511e-06 ;
	setAttr ".r" -type "double3" 0 0 -6.9566682270310768e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377365992004818e-07 -3.8842524126758077e-13 -4.030745943782958 ;
	setAttr ".bps" -type "matrix" 0.97694947265358456 -0.21333211096315313 0.007690143944552307 0
		 0.21332544659902614 0.97697973898370138 0.0016862528461221299 0 -0.0078728467029763084 -6.8804373971699989e-06 0.99996900863849258 0
		 66.459737163390997 93.84534202603902 -6.8166365896073398 1;
	setAttr ".radi" 0.57933899281065215;
	setAttr ".liw" yes;
createNode joint -n "R_midFinger04_JNT" -p "R_midFinger03_JNT";
	rename -uid "23616756-C243-0D27-31A0-F49FEEE9BBF1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.7877357798716247 -1.6215786757811657e-06 4.5747622756664441e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.97694947265358445 -0.21333211096315205 0.0076901439445522853 0
		 0.21332544659902597 0.97697973898370094 0.0016862528461221438 0 -0.0078728467029763136 -6.8804373971814313e-06 0.99996900863849303 0
		 68.836802925740216 93.326272748482069 -6.7979253067930241 1;
	setAttr ".radi" 0.57933899281065215;
	setAttr ".liw" yes;
createNode joint -n "R_pinky00_JNT";
	rename -uid "7E9732F9-2241-942A-F413-58BD52FC4EF1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -54.6404 93.7661 -11.2034 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -179.99999999995543 -4.3983581544585189 0.81686097833185201 ;
	setAttr ".bps" -type "matrix" 0.99983597708923799 -0.014244803417142312 -0.011185012007837569 5.4210108624275222e-20
		 0.014243989096213383 0.99989853761684988 -0.00015246740719870866 5.2041704279304213e-18
		 0.011186049018107014 -6.8767900297812016e-06 0.99993743417279468 -2.7078584532535914e-20
		 54.638483966584012 93.766223922580792 -11.346436045255002 0.99999999999999967;
	setAttr ".radi" 0.64155184490655581;
	setAttr ".liw" yes;
createNode joint -n "R_pinky01_JNT" -p "R_pinky00_JNT";
	rename -uid "D3EC01BD-BA4F-4A0D-2738-719452E4D98C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.7476165877896221 2.9707095990261223e-05 -6.447541839982307e-06 ;
	setAttr ".r" -type "double3" 4.9774476254058422e-10 -8.554406049520288e-11 5.6029326288368798e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0.49475199557195182 -2.9500150483996261 -6.4629190510614976 ;
	setAttr ".bps" -type "matrix" 0.99179361405910993 -0.12656974749284319 -0.018042342729345996 2.1684043449710089e-19
		 0.12654893553804997 0.99195771027415103 -0.0022951997411266856 -1.7347234759768071e-18
		 0.018187743833463936 -6.874820771912312e-06 0.99983458928313995 1.3234889800848443e-23
		 58.377480361268745 93.712953916459583 -11.388263625508271 0.99999999999999989;
	setAttr ".radi" 0.60562295843487834;
	setAttr ".liw" yes;
createNode joint -n "R_pinky02_JNT" -p "R_pinky01_JNT";
	rename -uid "296B4655-CD48-EDCC-7D61-798678322063";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.0446198258079065 -3.1341049421484968e-05 -7.2905492736197175e-05 ;
	setAttr ".r" -type "double3" 0 0 5.6003604400544788e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 2.3936693095581946e-16 3.2799470152584156e-14 0.83626176669899743 ;
	setAttr ".bps" -type "matrix" 0.99353419573159563 -0.11208539533488622 -0.01807390562644301 -3.2526065174565133e-18
		 0.11206697946415733 0.99369857809365891 -0.0020317500882971185 5.2041704279304213e-18
		 0.018187743833463992 -6.8748207718554057e-06 0.99983458928314084 1.3234889800848443e-23
		 61.396839273134454 93.327632323692995 -11.44319068648001 0.99999999999999978;
	setAttr ".radi" 0.56564578290185841;
	setAttr ".liw" yes;
createNode joint -n "R_pinky03_JNT" -p "R_pinky02_JNT";
	rename -uid "89F31C6A-BD48-0F0A-58BA-EAAC0BFA6B1E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2692965136398158 -2.045613113921263e-05 5.2571396018663563e-05 ;
	setAttr ".r" -type "double3" 0 0 5.5998013581768779e-12 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 3.6127339129190356e-17 3.7172732839388937e-14 0.11136891195842066 ;
	setAttr ".bps" -type "matrix" 0.99375029276816484 -0.11015238503007661 -0.018077823302913382 0
		 0.11013428892689825 0.99391471063915759 -0.0019965915064172196 0 0.018187743833463946 -6.874820771898917e-06 0.99983458928313906 0
		 63.651319184491655 93.07329354680472 -11.484203122015321 1;
	setAttr ".radi" 0.54911436848391437;
	setAttr ".liw" yes;
createNode joint -n "R_pinky04_JNT" -p "R_pinky03_JNT";
	rename -uid "00BD48D1-7248-51B7-1AC6-0994412215C5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0646996026908369 -2.8142975025957639e-06 2.5304754940336238e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99375029276816496 -0.11015238503007556 -0.018077823302913559 0
		 0.11013428892689792 0.99391471063915893 -0.0019965915064172335 0 0.018187743833463946 -6.874820771908314e-06 0.99983458928313906 0
		 65.600499112351741 92.857236435205223 -11.519661657804262 1;
	setAttr ".radi" 0.54911436848391437;
	setAttr ".liw" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "E0C0C032-B247-9412-1A11-6FB1199D8375";
	setAttr -s 53 ".lnk";
	setAttr -s 53 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "192547E1-2245-28D8-4F61-BAA4A27CC3FF";
	setAttr -s 3 ".dli[1:2]"  3 4;
createNode displayLayer -n "defaultLayer";
	rename -uid "D7986587-334F-4F0A-1889-9280477EAC4A";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "343F2D92-7444-B83A-ABFF-90894C6B8677";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "A081435F-A340-5679-E4BA-E88494A30A72";
	setAttr ".g" yes;
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "6CEFA34E-9141-AFF3-44FB-44A44A74F3F6";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "39894B52-9741-CC4A-C0A0-79ACD3962D74";
createNode materialInfo -n "hp_body:materialInfo3";
	rename -uid "49D54B44-124F-CA78-3161-CF971F3CE3A3";
createNode shadingEngine -n "hp_body:eye_layerSG";
	rename -uid "577CF68F-E74A-C0AB-16D4-41A957B8FB9B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo6";
	rename -uid "F3E0115B-2F44-EC64-533B-F18EECD77426";
createNode shadingEngine -n "hp_body:eye_corneaSG";
	rename -uid "BAE1BBEA-E74D-C7E3-23F9-6FB25B63678C";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo1";
	rename -uid "6148F695-2B44-A538-CA2E-B08203CF0B86";
createNode shadingEngine -n "hp_body:body_SG";
	rename -uid "B074E2B3-A549-81DC-67F6-BE86BC892C72";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
	setAttr ".aovs[0].aov_name" -type "string" "specular";
	setAttr ".aal" -type "attributeAlias" {"ai_aov_specular","aiCustomAOVs[0]"} ;
createNode materialInfo -n "hp_body:materialInfo2";
	rename -uid "E437511F-674E-AF6F-7688-D6BA48F56B27";
createNode shadingEngine -n "hp_body:aiStandardSurface2SG";
	rename -uid "A38FC38B-5249-973C-58F3-2CA230D3A376";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
	setAttr ".aovs[0].aov_name" -type "string" "specular";
	setAttr ".aal" -type "attributeAlias" {"ai_aov_specular","aiCustomAOVs[0]"} ;
createNode materialInfo -n "hp_body:materialInfo16";
	rename -uid "E9507421-8C46-152E-69CA-03899FEF9ADA";
createNode shadingEngine -n "hp_body:shoeSole_SG";
	rename -uid "0B54A107-7F46-B5C7-C9CE-C382BFE635D9";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo18";
	rename -uid "9CB5A182-1B42-171B-60C7-1F8087D3518F";
createNode shadingEngine -n "hp_body:shoeLaces_SG";
	rename -uid "F255E9CF-624C-1642-53F6-B0A4075AD4DD";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo17";
	rename -uid "C5D74EB5-7543-3843-BAD3-18BB941A0D66";
createNode shadingEngine -n "hp_body:shoeSoleRing_SG";
	rename -uid "91CD4508-194F-93FE-CE8E-82936802797B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo19";
	rename -uid "D7BCA3E3-A74F-570C-3343-1484DDB18D3B";
createNode shadingEngine -n "hp_body:shoeSock_SG";
	rename -uid "48552FE5-9C42-5844-3E4F-38A3642521FC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo15";
	rename -uid "D4D00AFC-6C4E-3337-DC8F-9C983C02DBCA";
createNode shadingEngine -n "hp_body:shoeBody_SG";
	rename -uid "8A3B6ADA-9540-7CCF-EAAF-578B5C36D13B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo20";
	rename -uid "EFE74D1D-834E-3945-00EE-F5A05348FD8E";
createNode shadingEngine -n "hp_body:jumperSG";
	rename -uid "D2EDC5EE-8141-F4F5-16FD-238D68B2F5CE";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo7";
	rename -uid "8A157946-684E-033A-66DC-8CB81719CB01";
createNode shadingEngine -n "hp_body:cloakSG";
	rename -uid "279C7761-2A4D-8120-9AD1-40955BCA8988";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo9";
	rename -uid "371A4230-7242-4090-40E4-7FB284CA14D0";
createNode shadingEngine -n "hp_body:shirtSG";
	rename -uid "30CBE560-AE4C-59D8-AF1E-DCAE195A0C4B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo10";
	rename -uid "59740864-8146-46B9-7E61-BDA6E0CB925E";
createNode shadingEngine -n "hp_body:tie_SG";
	rename -uid "4D07A575-BF44-0E3B-A80A-58BB655BDA87";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo11";
	rename -uid "699C167E-B84C-BE07-1379-F98517CEB4B8";
createNode shadingEngine -n "hp_body:pants_SG";
	rename -uid "4CF2A077-B84F-55F2-2AF7-EA8224511106";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo12";
	rename -uid "027BD51F-CF4B-FBD7-5488-33A1251E62D4";
createNode shadingEngine -n "hp_body:lining_SG";
	rename -uid "B57E0E9E-2543-F25A-3661-F5AE358B7AD8";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode shadingEngine -n "hp_body:lambert2SG";
	rename -uid "FF3FE342-3E42-641B-AC9D-07B62DD9F0DD";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo21";
	rename -uid "0B208F26-2844-949C-BC52-27B9AB54273A";
createNode shadingEngine -n "hp_body:teeth_SG";
	rename -uid "8A768BD8-6940-3962-DD20-07AB7071A369";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body:materialInfo22";
	rename -uid "FB436C60-4546-3A8D-3D2F-C59FB4C50BED";
createNode materialInfo -n "hp_body1:materialInfo3";
	rename -uid "C3FEBC96-274F-DEA1-57BF-4585ED13C9A5";
createNode shadingEngine -n "hp_body1:eye_layerSG";
	rename -uid "547E1AA6-8A43-2A1A-5D9B-7996DEF6C61F";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo6";
	rename -uid "81DE6CC7-4144-0127-C2D6-63AA0C2EE98B";
createNode shadingEngine -n "hp_body1:eye_corneaSG";
	rename -uid "DEA3A9F6-5947-83C8-A516-CE9FE8D1BD0E";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo1";
	rename -uid "388E4200-9A4E-A3EA-CB46-D7A9847BB085";
createNode shadingEngine -n "hp_body1:body_SG";
	rename -uid "0841429F-714C-B3A8-8623-ABB0F651E0A8";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
	setAttr ".aovs[0].aov_name" -type "string" "specular";
	setAttr ".aal" -type "attributeAlias" {"ai_aov_specular","aiCustomAOVs[0]"} ;
createNode materialInfo -n "hp_body1:materialInfo2";
	rename -uid "FAAF5E8D-AE4C-3F38-CAFC-C1BEC3253A62";
createNode shadingEngine -n "hp_body1:aiStandardSurface2SG";
	rename -uid "78A70BD5-224E-5E33-6A81-2F94C9E50DD7";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
	setAttr ".aovs[0].aov_name" -type "string" "specular";
	setAttr ".aal" -type "attributeAlias" {"ai_aov_specular","aiCustomAOVs[0]"} ;
createNode materialInfo -n "hp_body1:materialInfo16";
	rename -uid "2A99D33B-A843-1CC7-2151-D79A70DEFC72";
createNode shadingEngine -n "hp_body1:shoeSole_SG";
	rename -uid "DFA4B666-9249-1802-7555-02A58F9C4F3B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo18";
	rename -uid "B846DB30-E34A-BDD1-B02E-FF827B562FA1";
createNode shadingEngine -n "hp_body1:shoeLaces_SG";
	rename -uid "4FA1F59B-2D4A-B31D-6439-99B926C39707";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo17";
	rename -uid "E2D5EC25-2B40-36B0-CB62-BFBDD2DB0C86";
createNode shadingEngine -n "hp_body1:shoeSoleRing_SG";
	rename -uid "3F08B78F-9748-DD0E-7979-47BD68CE5EBC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo19";
	rename -uid "C1150E62-6840-BB6B-17B5-629AC26B8EB6";
createNode shadingEngine -n "hp_body1:shoeSock_SG";
	rename -uid "228823B4-DD4D-B547-C29D-02B37D5CDF52";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo15";
	rename -uid "1E403F1A-D049-29D7-334D-33A71C0B2EF6";
createNode shadingEngine -n "hp_body1:shoeBody_SG";
	rename -uid "7BEB47D0-9647-9E17-FE10-88AC9A0D5BD3";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo20";
	rename -uid "A45609A9-264D-CBA7-05DD-91AC69200356";
createNode shadingEngine -n "hp_body1:jumperSG";
	rename -uid "32A5DF2C-D944-C18B-C3DB-B19918F7F053";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo7";
	rename -uid "B9B917DB-8D40-CF1F-9753-8AA75A73273B";
createNode shadingEngine -n "hp_body1:cloakSG";
	rename -uid "2EC9E829-6740-D3B0-B642-3BB6A63807DF";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo9";
	rename -uid "016E727C-DF49-167C-896D-7ABCBD683E04";
createNode shadingEngine -n "hp_body1:shirtSG";
	rename -uid "9DEFC97B-604E-FBEA-7306-10B357B102D6";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo10";
	rename -uid "AF8F863F-AA43-9573-72F2-5995216ACE29";
createNode shadingEngine -n "hp_body1:tie_SG";
	rename -uid "EABDA297-564A-3680-4D35-DA833BF39C06";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo11";
	rename -uid "7C75B646-B34D-9226-D5E5-369DB2A4A3FE";
createNode shadingEngine -n "hp_body1:pants_SG";
	rename -uid "25E067A8-6548-E48C-176D-11B0365BC3DB";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo12";
	rename -uid "DE0268AE-6046-8720-F86B-40A4C006D63B";
createNode shadingEngine -n "hp_body1:lining_SG";
	rename -uid "488A83E7-AC47-C9E3-3B0A-47BB0FD19846";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode shadingEngine -n "hp_body1:lambert2SG";
	rename -uid "6E00A4B9-9B4A-7C28-DE47-58894E5CC258";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo21";
	rename -uid "0153A1F2-064D-BED6-FD5B-3B951F8114CB";
createNode shadingEngine -n "hp_body1:teeth_SG";
	rename -uid "C3F3048E-3C4B-4D1C-73EE-33B1575B925A";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body1:materialInfo22";
	rename -uid "AFDC755D-AA41-8F3C-F671-5BBE949C2B0A";
createNode materialInfo -n "hp_body2:materialInfo3";
	rename -uid "B9BA1637-CA46-8A1E-7B0E-34839936244F";
createNode shadingEngine -n "hp_body2:eye_layerSG";
	rename -uid "8B9C15E4-E741-0910-AA3E-9A9EB3D30054";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo6";
	rename -uid "BBAEC9AD-1749-1873-B7AE-C78E1FF720BD";
createNode shadingEngine -n "hp_body2:eye_corneaSG";
	rename -uid "372D9A5A-F243-DF60-1B90-6CB294C89765";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo1";
	rename -uid "AEE2EEBD-F54A-1B4B-4F72-07AA31103AFE";
createNode shadingEngine -n "hp_body2:body_SG";
	rename -uid "751FC098-4149-714B-E15F-4DA293368954";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
	setAttr ".aovs[0].aov_name" -type "string" "specular";
	setAttr ".aal" -type "attributeAlias" {"ai_aov_specular","aiCustomAOVs[0]"} ;
createNode materialInfo -n "hp_body2:materialInfo2";
	rename -uid "E4296777-8248-2F23-9AD2-97883A92F1A6";
createNode shadingEngine -n "hp_body2:aiStandardSurface2SG";
	rename -uid "59BC5132-D14F-0FFD-0C72-AA98A3A1C740";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
	setAttr ".aovs[0].aov_name" -type "string" "specular";
	setAttr ".aal" -type "attributeAlias" {"ai_aov_specular","aiCustomAOVs[0]"} ;
createNode materialInfo -n "hp_body2:materialInfo16";
	rename -uid "41726263-A242-2E7F-4D52-BBADD50DDB7F";
createNode shadingEngine -n "hp_body2:shoeSole_SG";
	rename -uid "0C0C43B2-6948-C9E0-C177-0D8CDACCBFD3";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo18";
	rename -uid "CE6FC73F-244E-81BE-E83D-E081829CB66B";
createNode shadingEngine -n "hp_body2:shoeLaces_SG";
	rename -uid "AB18968D-C445-F5DC-3B1F-B6B88D0AEF2C";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo17";
	rename -uid "995B1014-544C-6EBE-07E7-2F9496EFA4D6";
createNode shadingEngine -n "hp_body2:shoeSoleRing_SG";
	rename -uid "CBD4E88A-B346-C029-DB57-C3A1140A9D42";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo19";
	rename -uid "1123B624-FE42-3EEC-B164-CE8D34DF7E2E";
createNode shadingEngine -n "hp_body2:shoeSock_SG";
	rename -uid "300E3C38-5947-31CF-362D-3780BF8197EB";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo15";
	rename -uid "ACE87BEA-1E49-7A96-E67A-B08DEA9EB4C6";
createNode shadingEngine -n "hp_body2:shoeBody_SG";
	rename -uid "9BA8EEF6-7D44-2916-1899-259F0926C2F9";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo20";
	rename -uid "305DEB89-BD49-0AB4-776E-4E9623044351";
createNode shadingEngine -n "hp_body2:jumperSG";
	rename -uid "0969297E-7046-2E93-5901-308FA9A00292";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo7";
	rename -uid "D9DCADD7-8B47-8011-DD4F-7BA356EE166C";
createNode shadingEngine -n "hp_body2:cloakSG";
	rename -uid "01362C83-6D48-8404-C990-8DBEF7B5F329";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo9";
	rename -uid "47E2FAA4-2843-F804-7667-B481C3375685";
createNode shadingEngine -n "hp_body2:shirtSG";
	rename -uid "D39B7C95-2A4C-433E-F921-1387EABB3172";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo10";
	rename -uid "C73C8F3C-5A43-FF5A-1E1C-BFB3DE35CB22";
createNode shadingEngine -n "hp_body2:tie_SG";
	rename -uid "B92B77A6-BD44-4247-58BD-969B12B97E67";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo11";
	rename -uid "74A15865-644E-A4E5-D385-E4ADEDCE35AF";
createNode shadingEngine -n "hp_body2:pants_SG";
	rename -uid "0BACFFEF-624A-5C84-20F0-BB93CB01126C";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo12";
	rename -uid "235B5DB8-5446-C550-246B-4ABFDEBDB013";
createNode shadingEngine -n "hp_body2:lining_SG";
	rename -uid "E4F24685-FC48-B8C3-7D42-EF83B6947263";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode shadingEngine -n "hp_body2:lambert2SG";
	rename -uid "FFA66DB5-2F48-9F98-2217-2B94DA27EF58";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo21";
	rename -uid "CB0967CC-3A42-452D-F09A-968AC1FEBF15";
createNode shadingEngine -n "hp_body2:teeth_SG";
	rename -uid "6D9D52E1-944D-E614-1C1B-B4B86B3A146C";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "hp_body2:materialInfo22";
	rename -uid "A62F54E6-084E-C3ED-6215-13AFED68E458";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "E1BEB7D5-2D4D-7BDF-0419-3CA406F85B4E";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n"
		+ "            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n"
		+ "            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n"
		+ "            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 0\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n"
		+ "            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 254\n            -height 487\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n"
		+ "            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n"
		+ "            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n"
		+ "            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n"
		+ "                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n"
		+ "                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n"
		+ "                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n"
		+ "                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n"
		+ "                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n"
		+ "                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n"
		+ "                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n"
		+ "                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n"
		+ "                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n"
		+ "                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n"
		+ "\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 0\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 254\\n    -height 487\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 0\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 254\\n    -height 487\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "0F61041E-C94C-9DEA-C380-FEB25FB8CB33";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "5210552A-3349-837E-76F8-F9AD92B45D46";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -2893.4522659769177 -1234.2122513094355 ;
	setAttr ".tgi[0].vh" -type "double2" 2894.6427421200897 1233.0217751662644 ;
	setAttr -s 21 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -424.28570556640625;
	setAttr ".tgi[0].ni[0].y" 535.71429443359375;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 561.4285888671875;
	setAttr ".tgi[0].ni[1].y" 535.71429443359375;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" -338.57144165039062;
	setAttr ".tgi[0].ni[2].y" 281.42855834960938;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" -258.57144165039062;
	setAttr ".tgi[0].ni[3].y" -131.42857360839844;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" -338.57144165039062;
	setAttr ".tgi[0].ni[4].y" 154.28572082519531;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" -645.71429443359375;
	setAttr ".tgi[0].ni[5].y" -100;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" -338.57144165039062;
	setAttr ".tgi[0].ni[6].y" -100;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" -95.714286804199219;
	setAttr ".tgi[0].ni[7].y" 535.71429443359375;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 835.71429443359375;
	setAttr ".tgi[0].ni[8].y" -344.28570556640625;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" -31.428571701049805;
	setAttr ".tgi[0].ni[9].y" -100;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" -31.428571701049805;
	setAttr ".tgi[0].ni[10].y" 154.28572082519531;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" 275.71429443359375;
	setAttr ".tgi[0].ni[11].y" -354.28570556640625;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" 835.71429443359375;
	setAttr ".tgi[0].ni[12].y" 37.142856597900391;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" -752.85711669921875;
	setAttr ".tgi[0].ni[13].y" 535.71429443359375;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" -338.57144165039062;
	setAttr ".tgi[0].ni[14].y" -354.28570556640625;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" 100;
	setAttr ".tgi[0].ni[15].y" -30;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" 835.71429443359375;
	setAttr ".tgi[0].ni[16].y" -217.14285278320312;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" -31.428571701049805;
	setAttr ".tgi[0].ni[17].y" -354.28570556640625;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" 582.85711669921875;
	setAttr ".tgi[0].ni[18].y" 281.42855834960938;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" -645.71429443359375;
	setAttr ".tgi[0].ni[19].y" 281.42855834960938;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" 232.85714721679688;
	setAttr ".tgi[0].ni[20].y" 535.71429443359375;
	setAttr ".tgi[0].ni[20].nvs" 18304;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 53 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -k on ".mwc";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "C_spine00_JNT.s" "C_spine01_JNT.is";
connectAttr "C_spine01_JNT.s" "C_spine02_JNT.is";
connectAttr "C_spine02_JNT.s" "C_spine03_JNT.is";
connectAttr "C_spine03_JNT.s" "C_spine04_JNT.is";
connectAttr "L_leg00_JNT.s" "L_leg01_JNT.is";
connectAttr "L_leg01_JNT.s" "L_leg02_JNT.is";
connectAttr "L_leg02_JNT.s" "L_leg03_JNT.is";
connectAttr "L_leg03_JNT.s" "L_leg04_JNT.is";
connectAttr "L_arm00_JNT.s" "L_arm01_JNT.is";
connectAttr "L_arm01_JNT.s" "L_arm02_JNT.is";
connectAttr "L_arm02_JNT.s" "L_arm03_JNT.is";
connectAttr "L_arm03_JNT.s" "L_arm04_JNT.is";
connectAttr "R_arm00_JNT.s" "R_arm01_JNT.is";
connectAttr "R_arm01_JNT.s" "R_arm02_JNT.is";
connectAttr "R_arm02_JNT.s" "R_arm03_JNT.is";
connectAttr "R_arm03_JNT.s" "R_arm04_JNT.is";
connectAttr "R_leg00_JNT.s" "R_leg01_JNT.is";
connectAttr "R_leg01_JNT.s" "R_leg02_JNT.is";
connectAttr "R_leg02_JNT.s" "R_leg03_JNT.is";
connectAttr "R_leg03_JNT.s" "R_leg04_JNT.is";
connectAttr "C_neck00_JNT.s" "C_neck01_JNT.is";
connectAttr "C_neck00_JNT.rx" "C_neck01_JNT.rx";
connectAttr "C_neck01_JNT.s" "C_neck02_JNT.is";
connectAttr "C_neckWithTwist00_JNT.s" "C_neckWithTwist01_JNT.is";
connectAttr "L_index00_JNT.s" "L_index01_JNT.is";
connectAttr "L_index01_JNT.s" "L_index02_JNT.is";
connectAttr "L_index02_JNT.s" "L_index03_JNT.is";
connectAttr "L_index03_JNT.s" "L_index04_JNT.is";
connectAttr "L_thumb00_JNT.s" "L_thumb01_JNT.is";
connectAttr "L_thumb01_JNT.s" "L_thumb02_JNT.is";
connectAttr "L_thumb02_JNT.s" "L_thumb03_JNT.is";
connectAttr "L_ring00_JNT.s" "L_ring01_JNT.is";
connectAttr "L_ring01_JNT.s" "L_ring02_JNT.is";
connectAttr "L_ring02_JNT.s" "L_ring03_JNT.is";
connectAttr "L_ring03_JNT.s" "L_ring04_JNT.is";
connectAttr "L_midFinger00_JNT.s" "L_midFinger01_JNT.is";
connectAttr "L_midFinger01_JNT.s" "L_midFinger02_JNT.is";
connectAttr "L_midFinger02_JNT.s" "L_midFinger03_JNT.is";
connectAttr "L_midFinger03_JNT.s" "L_midFinger04_JNT.is";
connectAttr "L_pinky00_JNT.s" "L_pinky01_JNT.is";
connectAttr "L_pinky01_JNT.s" "L_pinky02_JNT.is";
connectAttr "L_pinky02_JNT.s" "L_pinky03_JNT.is";
connectAttr "L_pinky03_JNT.s" "L_pinky04_JNT.is";
connectAttr "R_index00_JNT.s" "R_index01_JNT.is";
connectAttr "R_index01_JNT.s" "R_index02_JNT.is";
connectAttr "R_index02_JNT.s" "R_index03_JNT.is";
connectAttr "R_index03_JNT.s" "R_index04_JNT.is";
connectAttr "R_thumb00_JNT.s" "R_thumb01_JNT.is";
connectAttr "R_thumb01_JNT.s" "R_thumb02_JNT.is";
connectAttr "R_thumb02_JNT.s" "R_thumb03_JNT.is";
connectAttr "R_ring00_JNT.s" "R_ring01_JNT.is";
connectAttr "R_ring01_JNT.s" "R_ring02_JNT.is";
connectAttr "R_ring02_JNT.s" "R_ring03_JNT.is";
connectAttr "R_ring03_JNT.s" "R_ring04_JNT.is";
connectAttr "R_midFinger00_JNT.s" "R_midFinger01_JNT.is";
connectAttr "R_midFinger01_JNT.s" "R_midFinger02_JNT.is";
connectAttr "R_midFinger02_JNT.s" "R_midFinger03_JNT.is";
connectAttr "R_midFinger03_JNT.s" "R_midFinger04_JNT.is";
connectAttr "R_pinky00_JNT.s" "R_pinky01_JNT.is";
connectAttr "R_pinky01_JNT.s" "R_pinky02_JNT.is";
connectAttr "R_pinky02_JNT.s" "R_pinky03_JNT.is";
connectAttr "R_pinky03_JNT.s" "R_pinky04_JNT.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:jumperSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:cloakSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:shirtSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:tie_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:pants_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:lining_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:shoeBody_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:shoeSole_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:shoeSoleRing_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:shoeLaces_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:shoeSock_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:body_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:aiStandardSurface2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:eye_layerSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:eye_corneaSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:lambert2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body:teeth_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:jumperSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:cloakSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:shirtSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:tie_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:pants_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:lining_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:shoeBody_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:shoeSole_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:shoeSoleRing_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:shoeLaces_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:shoeSock_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:body_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:aiStandardSurface2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:eye_layerSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:eye_corneaSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:lambert2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body1:teeth_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:jumperSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:cloakSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:shirtSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:tie_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:pants_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:lining_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:shoeBody_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:shoeSole_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:shoeSoleRing_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:shoeLaces_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:shoeSock_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:body_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:aiStandardSurface2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:eye_layerSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:eye_corneaSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:lambert2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "hp_body2:teeth_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:jumperSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:cloakSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:shirtSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:tie_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:pants_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:lining_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:shoeBody_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:shoeSole_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:shoeSoleRing_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:shoeLaces_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:shoeSock_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:body_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:aiStandardSurface2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:eye_layerSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:eye_corneaSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body:teeth_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:jumperSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:cloakSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:shirtSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:tie_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:pants_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:lining_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:shoeBody_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:shoeSole_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:shoeSoleRing_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:shoeLaces_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:shoeSock_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:body_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:aiStandardSurface2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:eye_layerSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:eye_corneaSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body1:teeth_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:jumperSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:cloakSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:shirtSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:tie_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:pants_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:lining_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:shoeBody_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:shoeSole_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:shoeSoleRing_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:shoeLaces_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:shoeSock_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:body_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:aiStandardSurface2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:eye_layerSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:eye_corneaSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "hp_body2:teeth_SG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "hp_body:eye_layerSG.msg" "hp_body:materialInfo3.sg";
connectAttr "hp_body:eye_corneaSG.msg" "hp_body:materialInfo6.sg";
connectAttr "hp_body:body_SG.msg" "hp_body:materialInfo1.sg";
connectAttr "hp_body:aiStandardSurface2SG.msg" "hp_body:materialInfo2.sg";
connectAttr "hp_body:shoeSole_SG.msg" "hp_body:materialInfo16.sg";
connectAttr "hp_body:shoeLaces_SG.msg" "hp_body:materialInfo18.sg";
connectAttr "hp_body:shoeSoleRing_SG.msg" "hp_body:materialInfo17.sg";
connectAttr "hp_body:shoeSock_SG.msg" "hp_body:materialInfo19.sg";
connectAttr "hp_body:shoeBody_SG.msg" "hp_body:materialInfo15.sg";
connectAttr "hp_body:jumperSG.msg" "hp_body:materialInfo20.sg";
connectAttr "hp_body:cloakSG.msg" "hp_body:materialInfo7.sg";
connectAttr "hp_body:shirtSG.msg" "hp_body:materialInfo9.sg";
connectAttr "hp_body:tie_SG.msg" "hp_body:materialInfo10.sg";
connectAttr "hp_body:pants_SG.msg" "hp_body:materialInfo11.sg";
connectAttr "hp_body:lining_SG.msg" "hp_body:materialInfo12.sg";
connectAttr "hp_body:lambert2SG.msg" "hp_body:materialInfo21.sg";
connectAttr "hp_body:teeth_SG.msg" "hp_body:materialInfo22.sg";
connectAttr "hp_body1:eye_layerSG.msg" "hp_body1:materialInfo3.sg";
connectAttr "hp_body1:eye_corneaSG.msg" "hp_body1:materialInfo6.sg";
connectAttr "hp_body1:body_SG.msg" "hp_body1:materialInfo1.sg";
connectAttr "hp_body1:aiStandardSurface2SG.msg" "hp_body1:materialInfo2.sg";
connectAttr "hp_body1:shoeSole_SG.msg" "hp_body1:materialInfo16.sg";
connectAttr "hp_body1:shoeLaces_SG.msg" "hp_body1:materialInfo18.sg";
connectAttr "hp_body1:shoeSoleRing_SG.msg" "hp_body1:materialInfo17.sg";
connectAttr "hp_body1:shoeSock_SG.msg" "hp_body1:materialInfo19.sg";
connectAttr "hp_body1:shoeBody_SG.msg" "hp_body1:materialInfo15.sg";
connectAttr "hp_body1:jumperSG.msg" "hp_body1:materialInfo20.sg";
connectAttr "hp_body1:cloakSG.msg" "hp_body1:materialInfo7.sg";
connectAttr "hp_body1:shirtSG.msg" "hp_body1:materialInfo9.sg";
connectAttr "hp_body1:tie_SG.msg" "hp_body1:materialInfo10.sg";
connectAttr "hp_body1:pants_SG.msg" "hp_body1:materialInfo11.sg";
connectAttr "hp_body1:lining_SG.msg" "hp_body1:materialInfo12.sg";
connectAttr "hp_body1:lambert2SG.msg" "hp_body1:materialInfo21.sg";
connectAttr "hp_body1:teeth_SG.msg" "hp_body1:materialInfo22.sg";
connectAttr "hp_body2:eye_layerSG.msg" "hp_body2:materialInfo3.sg";
connectAttr "hp_body2:eye_corneaSG.msg" "hp_body2:materialInfo6.sg";
connectAttr "hp_body2:body_SG.msg" "hp_body2:materialInfo1.sg";
connectAttr "hp_body2:aiStandardSurface2SG.msg" "hp_body2:materialInfo2.sg";
connectAttr "hp_body2:shoeSole_SG.msg" "hp_body2:materialInfo16.sg";
connectAttr "hp_body2:shoeLaces_SG.msg" "hp_body2:materialInfo18.sg";
connectAttr "hp_body2:shoeSoleRing_SG.msg" "hp_body2:materialInfo17.sg";
connectAttr "hp_body2:shoeSock_SG.msg" "hp_body2:materialInfo19.sg";
connectAttr "hp_body2:shoeBody_SG.msg" "hp_body2:materialInfo15.sg";
connectAttr "hp_body2:jumperSG.msg" "hp_body2:materialInfo20.sg";
connectAttr "hp_body2:cloakSG.msg" "hp_body2:materialInfo7.sg";
connectAttr "hp_body2:shirtSG.msg" "hp_body2:materialInfo9.sg";
connectAttr "hp_body2:tie_SG.msg" "hp_body2:materialInfo10.sg";
connectAttr "hp_body2:pants_SG.msg" "hp_body2:materialInfo11.sg";
connectAttr "hp_body2:lining_SG.msg" "hp_body2:materialInfo12.sg";
connectAttr "hp_body2:lambert2SG.msg" "hp_body2:materialInfo21.sg";
connectAttr "hp_body2:teeth_SG.msg" "hp_body2:materialInfo22.sg";
connectAttr "L_midFinger01_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "L_midFinger04_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "L_pinky01_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "C_spine_CRV.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "L_ring01_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "L_index00_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn";
connectAttr "L_index01_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr "L_midFinger02_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "R_heel_LTRShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn";
connectAttr "L_index02_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn";
connectAttr "L_ring02_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn";
connectAttr "L_thumb02_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn";
connectAttr "R_ballFoot_LTR.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "L_midFinger00_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "L_thumb00_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn";
connectAttr "uiConfigurationScriptNode.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn"
		;
connectAttr "R_heel_LTR.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn";
connectAttr "L_thumb01_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn";
connectAttr "L_pinky04_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn";
connectAttr "L_pinky00_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn";
connectAttr "L_midFinger03_JNT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "hp_body:jumperSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:cloakSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:shirtSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:tie_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:pants_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:lining_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:shoeBody_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:shoeSole_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:shoeSoleRing_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:shoeLaces_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:shoeSock_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:body_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:aiStandardSurface2SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:eye_layerSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:eye_corneaSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body:teeth_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:jumperSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:cloakSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:shirtSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:tie_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:pants_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:lining_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:shoeBody_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:shoeSole_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:shoeSoleRing_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:shoeLaces_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:shoeSock_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:body_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:aiStandardSurface2SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:eye_layerSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:eye_corneaSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body1:teeth_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:jumperSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:cloakSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:shirtSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:tie_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:pants_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:lining_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:shoeBody_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:shoeSole_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:shoeSoleRing_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:shoeLaces_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:shoeSock_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:body_SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:aiStandardSurface2SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:eye_layerSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:eye_corneaSG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "hp_body2:teeth_SG.pa" ":renderPartition.st" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of hp_guides.ma
