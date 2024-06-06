$(function () {

    // Mapping between evaluatees and positions
    const evaluateePositionMap = {
        "VAN ELLIS V. MERCADO": "PRESIDENT",
        "HANS CHRISTIAN O. ANCIERTO": "VP - INTERNAL",
        "JOLO MARCO B. RAMOS": "VP - EXTERNAL",
        "KARYLLE D. DELICANA": "SECRETARY",
        "DJERRAMAINE MARIE RAMOS": "TREASURER",
        "RHODA MAE C. PALEN": "AUDITOR",
        "MIRALUNA DELA PEÑA": "P.R.O.",
        "ALEX S. COSTA JR.": "SAP",
        "AUBRIANA CHANELLE M BUYO": "SAP",
        "CHERRY BELLE R. GILANA": "SAP",
        "EDGSEL G. SOLICITO": "SAP",
        "KARL FIOLO S. CALMA": "SAP",
        "LOUBERT L. APIN": "SAP",
        "MARIA EUNILA A. ORCASITAS": "SAP",
        "TRACY MARGARETTE R. RAMENTO": "SAP",
        "XENALYN S. BELENCIO": "SAP",
        "CARL JUSTIN I. JUNTILLA": "DOCU COMM",
        "CLINTON MALICDON": "DOCU COMM",
        "JULLIANE FAYE C. CORDERO": "DOCU COMM",
        "RIO YSABEL O. ESTOPACE": "STRAAW COMM",
        "ARNIE MONICA A. DEL ROSARIO": "PROPERTY COMM",
        "CHRISLYNNE SALAS": "CIRCULATION COMM",
        "KRIZIA MAE C. TOLENTINO": "CREATIVES COMM",
        "MARJURIE ANNE A. GUIEB": "CREATIVES COMM",
        "DAVE KENNETH C. TORRES": "TECHNICAL COMM",
        "JESSEL ANDREA D. MORALEDA": "SOCENVI COMM"
    };

    // Populate the evaluatee dropdown
    const evaluateeSelect = $('#evaluatee');
    evaluateeSelect.append($('<option>', {
        value: '',
        text: 'Select Evaluatee'
    }));

    for (const evaluatee in evaluateePositionMap) {
        if (evaluateePositionMap.hasOwnProperty(evaluatee)) {
            $('#evaluatee').append($('<option>', {
                value: evaluatee,
                text: evaluatee
            }));
        }
    }

    // When an evaluatee is selected, autofill the position
    $('#evaluatee').change(function () {
        const selectedEvaluatee = $(this).val();
        const position = evaluateePositionMap[selectedEvaluatee];
        $('#position').val(position);
    });

    // Trigger change event on page load to autofill position if an evaluatee is pre-selected
    $('#evaluatee').change();

})