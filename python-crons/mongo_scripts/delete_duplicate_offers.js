db.getCollection('offers').aggregate([
    {
        $match: {
            'id': {'$in':  [ 
        3011095, 
        2970041, 
        4010968, 
        4717459, 
        4514525, 
        1716157, 
        3784615, 
        4422636, 
        4463175, 
        4760326, 
        4939811, 
        4756872, 
        2046469, 
        3891134, 
        4773622, 
        4522304, 
        4514108, 
        3898625, 
        3177688, 
        2861747
    ]}
        }
    },
    {
        '$project': {
            'id': 1
        }
    },
    {
        '$group': {
            '_id': '$id',
            'id_to_delete': {$first: '$_id'}
        }
    },
    {
        '$group': {
            _id: null,
            tab: {$push: '$id_to_delete'}
        }
    }
])
db.getCollection('offers').find({_id: {$in:[ 
        ObjectId("5d3f654c54e90016033a7c6d"), 
        ObjectId("5d3f654c54e90016033a7c6b"), 
        ObjectId("5d3f654c54e90016033a7c6a"), 
        ObjectId("5d3f654c54e90016033a7c69"), 
        ObjectId("5d3f654c54e90016033a7c65"), 
        ObjectId("5d3f654c54e90016033a7c64"), 
        ObjectId("5d3f654c54e90016033a7c5d"), 
        ObjectId("5d3f654c54e90016033a7c5b"), 
        ObjectId("5d3f654c54e90016033a7c67"), 
        ObjectId("5d3f654c54e90016033a7c5a"), 
        ObjectId("5d3f654c54e90016033a7c61"), 
        ObjectId("5d3f654c54e90016033a7c5e"), 
        ObjectId("5d3f654c54e90016033a7c6c"), 
        ObjectId("5d3f654c54e90016033a7c68"), 
        ObjectId("5d3f654c54e90016033a7c66"), 
        ObjectId("5d3f654c54e90016033a7c5c"), 
        ObjectId("5d3f654c54e90016033a7c62"), 
        ObjectId("5d3f654c54e90016033a7c5f"), 
        ObjectId("5d3f654c54e90016033a7c60"), 
        ObjectId("5d3f654c54e90016033a7c63")
    ]}})