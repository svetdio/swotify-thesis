$(function () {

    // Mapping between evaluatees and positions
    const evaluateePositionMap = {
        "SIRC LAURENCE D. CERRERA": "PRESIDENT",
        "VINCENT S. CACHAPERO": "VICE PRESIDENT",
        "MA. ANGELICA M. RUBRICO": "SECRETARY",
        "ARYNE KATE B. MAGLASANG": "TREASURER",
        "JANE GAUFO ADELAIDE": "AUDITOR",
        "JOANA TOVI TADURAN": "PUBLIC RELATIONS OFFICER",
        "JADERYAN L. BLANCAFLOR": "GENDER AND DEVELOPMENT",
        "JOHN PAUL YAP": "1ST YEAR REPRESENTATIVE",
        "NICOLE SHANE DANTIS": "2ND YEAR REPRESENTATIVE",
        "JOHN PAUL A. MAGNO": "3RD YEAR REPRESENTATIVE",
        "ROMEO C. COBRETA JR.": "4TH YEAR REPRESENTATIVE",
        "RENZ ANDREI A. PAMBUENA": "BITS CREATIVE COMMITTEE",
        "CLARRISE ANNE SARDOMA": "BITS CREATIVE COMMITTEE",
        "KYLE ADRIELLE D. MALIWANAG": "BITS CREATIVE COMMITTEE",
        "CHRISTOFF JEAN REYES": "BITS DOCUMENTATION COMMITTEE",
        "IVAN DURAN": "BITS DOCUMENTATION COMMITTEE",
        "LOEL CAMPANA": "BITS DOCUMENTATION COMMITTEE",
        "RAILEE BABIANO": "BITS TECHNICAL COMMITTEE",
        "PAUL JUSTIN DELA CUESTA": "BITS TECHNICAL COMMITTEE",
        "SHAINA MAY YUSORES": "BITS SECRETARIAT COMMITTEE"
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