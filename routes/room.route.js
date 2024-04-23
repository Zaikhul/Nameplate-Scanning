const express = require('express')
const router = express.Router()
const { Get, Insert, GetByPK, Update, Delete } = require('../controller/room.controller')
const { CheckPostRoom } = require('../middleware/middleware')

router.get('/', Get)
router.get('/:roomId', GetByPK)
router.post('/', CheckPostRoom, Insert)
router.put('/:roomId', Update)
router.delete('/:roomId', Delete)
module.exports = router