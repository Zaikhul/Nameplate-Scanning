const express = require('express')
const router = express.Router()
const userRoute = require('./user.route')
const roomRoute = require('./room.route')
const roomCodeRoute = require('./room_code.route')
const roomNameRoute = require('./room_name.route')
const roomNamaRoute = require('./room_nama.route')
const roominformRoute = require('./room_inform.route')
const roomlectureRoute = require('./room_lecture.route')
const roomstudentRoute = require('./room_student.route')
const recordRoute = require('./record.route')
const morgan = require('morgan')

router.use(morgan('dev'))
router.get('/ping', (req, res) => {
    const pong = 'PING' || 'void'
    res.render('index', {
        pong
    })
    return
})

router.post('/signup', (req, res) => {
    const pong = 'PING' || 'void'
    res.render('register')
    return
})

router.use('/users', userRoute)
router.use('/room', roomRoute)
router.use('/room_code', roomCodeRoute)
router.use('/room_name', roomNameRoute)
router.use('/room_nama', roomNamaRoute)
router.use('/roominform', roominformRoute)
router.use('/roomlecture', roomlectureRoute)
router.use('/roomstudent', roomstudentRoute)
router.use('/record', recordRoute)



module.exports = router