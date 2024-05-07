const express = require('express')

const app = express()

app.get('/', (_req, res) => {
 res.send(`
  Test Terraform ${new Date().toISOString()}.
 `)
})

app.listen(process.env.PORT, () => {
 console.log(`Listening on port ${process.env.PORT}`)
})
