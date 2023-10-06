from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {"msg":"fastapi"}

@app.get('/names')
async def names():
    return {0:'Salman',1:'AnotherOne',3:'OneMore'}

@app.get('/more/deep/url')
async def deep():
    return {"name":"is bond"}