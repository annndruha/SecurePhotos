import QtQuick 2.4

Item {
    width: 400
    height: 400

    Row {
        id: row
        x: 0
        y: 0
        width: 200
        height: 400
    }

    Rectangle {
        id: rectangle
        x: 45
        y: 100
        width: 200
        height: 200
        color: "#ffffff"

        Text {
            id: element
            text: qsTr("Text")
            anchors.fill: parent
            font.pixelSize: 12
        }
    }
}

/*##^##
Designer {
    D{i:3;anchors_x:102;anchors_y:49}
}
##^##*/
