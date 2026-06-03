// Students Analytics

const studentsCtx =
document.getElementById(
'studentsChart'
);

new Chart(studentsCtx, {

    type: 'bar',

    data: {

        labels: [

            'Students',

            'Classes',

            'Subjects',

            'Attendance',

            'Fees'
        ],

        datasets: [{

            label: 'ERP Analytics',

            data: [

                TOTAL_STUDENTS,

                TOTAL_CLASSES,

                TOTAL_SUBJECTS,

                TOTAL_ATTENDANCE,

                TOTAL_FEES
            ],

            backgroundColor: [

                '#3b82f6',

                '#22c55e',

                '#f59e0b',

                '#ef4444',

                '#8b5cf6'
            ],

            borderRadius: 10
        }]
    },

    options: {

        responsive:true
    }
});

// Attendance Analytics

const attendanceCtx =
document.getElementById(
'attendanceChart'
);

new Chart(attendanceCtx, {

    type:'doughnut',

    data:{

        labels:[
            'Attendance',
            'Students'
        ],

        datasets:[{

            data:[
                TOTAL_ATTENDANCE,
                TOTAL_STUDENTS
            ],

            backgroundColor:[
                '#3b82f6',
                '#22c55e'
            ]
        }]
    },

    options:{
        responsive:true
    }
});