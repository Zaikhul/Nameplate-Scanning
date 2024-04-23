const express = require('express')
const router = express.Router()
const { Get, Insert, GetByPK, Update, Delete } = require('../controller/room_inform.controller')
const { CheckPostRoomInform } = require('../middleware/middleware')

router.get('/', Get)
router.get('/:roomInformId', GetByPK)
router.post('/', CheckPostRoomInform, Insert)
router.put('/:roomInformId', Update)
router.delete('/:roomInformId', Delete)
module.exports = router