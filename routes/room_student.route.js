const express = require('express')
const router = express.Router()
const { Get, Insert, GetByPK, Update, Delete } = require('../controller/room_student.controller')
const { CheckPostRoomStudent } = require('../middleware/middleware')

router.get('/', Get)
router.get('/:roomstudentId', GetByPK)
router.post('/', CheckPostRoomStudent, Insert)
router.put('/:roomstudentId', Update)
router.delete('/:roomstudentId', Delete)
module.exports = router