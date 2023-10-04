db.createUser(
    {
        user    : "StreamServ",
        pwd     : "StreamServ",
        roles   : [
            {
                role: "readWrite",
                db  : "StreamServ"
            }
        ]    
    }
)