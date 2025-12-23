#include "augmentator.hpp"
#include <string>
int main(){
    std::vector<std::string> label_names{"fish","tail"};
    //pairs of img_info and their labels
    std::vector<std::pair<std::string,std::string>> imId_labels{
      {R"(
    {
      "image_id": "194ecd55-55a9-4e6b-a8ba-00461cbeb497",
      "rel_path": "frame_00000 – kopija – kopija – kopija.jpg",
      "version_id": "9f058990-3a9f-46b3-b1d7-4964fa61325f",
      "augmentations": {
        "rotation": [
          90,
          -90,
          -45,
          73,
          15
        ],
        "brightness": [
          1,
          100
        ]
      }
    }
)",
        R"({
  "version": "3.3.0-beta.2",
  "flags": {},
  "shapes": [
    {
      "label": "fish",
      "score": 0.9196167588233948,
      "points": [
        [
          763.1216888427734,
          288.7421245574951
        ],
        [
          891.9194641113281,
          288.7421245574951
        ],
        [
          891.9194641113281,
          738.8219299316406
        ],
        [
          763.1216888427734,
          738.8219299316406
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.9156639575958252,
      "points": [
        [
          478.3221435546875,
          209.29829788208008
        ],
        [
          569.9114074707031,
          209.29829788208008
        ],
        [
          569.9114074707031,
          472.6800117492676
        ],
        [
          478.3221435546875,
          472.6800117492676
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.9155949950218201,
      "points": [
        [
          1076.524169921875,
          375.1875305175781
        ],
        [
          1204.5297393798828,
          375.1875305175781
        ],
        [
          1204.5297393798828,
          677.3045806884766
        ],
        [
          1076.524169921875,
          677.3045806884766
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.9131847023963928,
      "points": [
        [
          893.2580299377441,
          195.26277923583984
        ],
        [
          1004.608081817627,
          195.26277923583984
        ],
        [
          1004.608081817627,
          455.7364311218262
        ],
        [
          893.2580299377441,
          455.7364311218262
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.9064587950706482,
      "points": [
        [
          423.354434967041,
          608.8447303771973
        ],
        [
          515.0805320739746,
          608.8447303771973
        ],
        [
          515.0805320739746,
          884.6083564758301
        ],
        [
          423.354434967041,
          884.6083564758301
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.9025569558143616,
      "points": [
        [
          565.5014228820801,
          407.6675796508789
        ],
        [
          671.2125205993652,
          407.6675796508789
        ],
        [
          671.2125205993652,
          702.8331146240234
        ],
        [
          565.5014228820801,
          702.8331146240234
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "tail",
      "score": 0.8991742730140686,
      "points": [
        [
          278.40223693847656,
          903.7555999755859
        ],
        [
          386.9123840332031,
          903.7555999755859
        ],
        [
          386.9123840332031,
          1020.4477233886719
        ],
        [
          278.40223693847656,
          1020.4477233886719
        ]
      ],
      "group_id": null,
      "description": "",
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.8883923888206482,
      "points": [
        [
          208.28250795252183,
          624.15950236601
        ],
        [
          387.94117647058823,
          624.15950236601
        ],
        [
          387.94117647058823,
          1000.6470588235298
        ],
        [
          208.28250795252183,
          1000.6470588235298
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.8845413327217102,
      "points": [
        [
          937.8064422607422,
          490.0068550109863
        ],
        [
          996.5871276855469,
          490.0068550109863
        ],
        [
          996.5871276855469,
          669.2853126525879
        ],
        [
          937.8064422607422,
          669.2853126525879
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.8588638305664062,
      "points": [
        [
          705.2468910217285,
          149.06737518310547
        ],
        [
          776.8146705627441,
          149.06737518310547
        ],
        [
          776.8146705627441,
          331.481258392334
        ],
        [
          705.2468910217285,
          331.481258392334
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "tail",
      "score": 0.8554453253746033,
      "points": [
        [
          665.2563858032227,
          916.2421798706055
        ],
        [
          766.5241012573242,
          916.2421798706055
        ],
        [
          766.5241012573242,
          1021.7113876342773
        ],
        [
          665.2563858032227,
          1021.7113876342773
        ]
      ],
      "group_id": null,
      "description": "",
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "tail",
      "score": 0.80939781665802,
      "points": [
        [
          842.342658996582,
          946.2073516845703
        ],
        [
          937.0059356689453,
          946.2073516845703
        ],
        [
          937.0059356689453,
          1022.8069610595703
        ],
        [
          842.342658996582,
          1022.8069610595703
        ]
      ],
      "group_id": null,
      "description": "",
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    },
    {
      "label": "fish",
      "score": 0.7996468544006348,
      "points": [
        [
          878.4890594482422,
          379.06535720825195
        ],
        [
          938.4629821777344,
          379.06535720825195
        ],
        [
          938.4629821777344,
          561.5284614562988
        ],
        [
          878.4890594482422,
          561.5284614562988
        ]
      ],
      "group_id": null,
      "description": null,
      "difficult": false,
      "shape_type": "rectangle",
      "flags": {},
      "attributes": {},
      "kie_linking": []
    }
  ],
  "imagePath": "frame_00000.jpg",
  "imageData": null,
  "imageHeight": 1024,
  "imageWidth": 1360
})"}
};
    process_json(imId_labels,R"(C:\Users\josip\Pictures\Fish)",R"(C:\Users\josip\Pictures\Camera Roll)",label_names);
    return 0;
}