const express = require('express')
const router = express.Router()
const { Get, Insert, GetByPK, Update, Delete } = require('../controller/room_lecture.controller')
const { CheckPostRoomLecture } = require('../middleware/middleware')

router.get('/', Get)
router.get('/:roomLectureId', GetByPK)
router.post('/', CheckPostRoomLecture, Insert)
router.put('/:roomLectureId', Update)
router.delete('/:roomLectureId', Delete)
module.exports = router