const express = require('express')
const router = express.Router()
const { Get, Insert, GetByPK, Update, Delete } = require('../controller/user.controller')
const { CheckPostReq } = require('../middleware/middleware')

router.get('/', Get)
router.get('/:userId', GetByPK)
router.post('/', CheckPostReq, Insert)
router.put('/:userId', Update)
router.delete('/:userId', Delete)
module.exports = router