window.addEventListener('load', () =>
{
    var frame = document.getElementById('frame');
    var fixButton = document.getElementById('fix');
    frame.innerHTML = PrintTile(prdTile);
    fixButton.addEventListener('click', () =>
    {
        switchFixMode();
    }, false);
}, false);

var width = 10;
var height = 10;
var colors = 3;
var ansTile = initTileRand(width, height, colors);
var prdTile = initTile(width, height);
var prdFixTile = initTile(width, height);
var fixModeIsOn = false;

function switchFixMode()
{
    fixModeIsOn = !fixModeIsOn;
    frame.innerHTML = PrintTile(prdTile);
    if (CheckAns(prdTile, ansTile)) frame.innerHTML += "OK";
}

function initTile(width, height)
{
    var tile = [];
    for (y = 0; y < height; y++)
    {
        var row = [];
        for (x = 0; x < width; x++)
        {
            row.push(0);
        }
        tile.push(row);
    }
    return tile;
}

function initTileRand(width, height, randWidth)
{
    var tile = [];
    for (y = 0; y < height; y++)
    {
        var row = [];
        for (x = 0; x < width; x++)
        {
            //var value = Math.floor(Math.random() * randWidth);
            var value = Math.floor(Math.random() * (randWidth * 2 - 1)) + 1;
            value = Math.floor(value / 2);
            row.push(value);
        }
        tile.push(row);
    }
    return tile;
}

function Contains(tile, x, y)
{
    if (isNaN(x) || isNaN(y)) return false;
    //console.log(JSON.stringify(x));
    //console.log(JSON.stringify(y));

    var width = tile[0].length;
    if (x < 0 || width <= x) return false;

    var height = tile.length;
    if (y < 0 || height <= y) return false;

    return true;
}

function CheckAns(prdTile, ansTile)
{
    width = ansTile[0].length;
    height = ansTile.length;
    for (y = 0; y < height; y++)
    {
        var prdRow = prdTile[y];
        var ansRow = ansTile[y];
        for (x = 0; x < width; x++)
        {
            if (prdRow[x] != ansRow[x]) return false;
        }
    }
    return true;
}

function OpenTile(tile, x, y)
{
    var cell = tile[y][x];
    tile[y][x] = (cell + 1) % colors;

    frame.innerHTML = PrintTile(tile);
    if (CheckAns(prdTile, ansTile)) frame.innerHTML += "OK";
}

function SetFixTile(tile, x, y)
{
    var cell = tile[y][x];
    tile[y][x] = !cell;

    frame.innerHTML = PrintTile(prdTile);
    if (CheckAns(prdTile, ansTile)) frame.innerHTML += "OK";
}

function GetHintX(tile, y)
{
    var row = tile[y];
    var width = row.length;
    var hints = Array(width);
    var index = -1;
    var oldColor = -1;
    for (x = 0; x < width; x++)
    {
        var nowColor = row[x];
        if (nowColor >= 1)
        {
            if (nowColor != oldColor)
            {
                index++;
                hints[index] = {
                    color: nowColor,
                    len: 0
                };
            }
            hints[index].len++;
        }
        oldColor = nowColor;
    }
    //console.log(JSON.stringify(hints));
    return hints;
}

function GetHintsY(tile)
{
    var width = tile[0].length;
    var height = tile.length;
    var fullHints = Array(width);
    for (x = 0; x < width; x++)
    {
        var hints = Array(height);
        var index = -1;
        var oldColor = -1;
        for (y = 0; y < height; y++)
        {
            var nowColor = tile[y][x];
            if (nowColor >= 1)
            {
                if (nowColor != oldColor)
                {
                    index++;
                    hints[index] = {
                        color: nowColor,
                        len: 0
                    };
                }
                hints[index].len++;
            }
            oldColor = nowColor;
        }
        fullHints[x] = hints;
        //console.log(JSON.stringify(hints));
    }
    return fullHints;
}

function PrintColor(color)
{
    switch (color)
    {
        case 0:
            return '#e0e0e0';
        case 1:
            return '#e04040';
        case 2:
            return '#4040e0';
        case 3:
            return '#008000';
        case 4:
            return '#808000';
        case 5:
            return '#800080';
        case 6:
            return '#008080';
    }
}

function PrintCell(cell, fixCell, x, y)
{
    var text;
    var color;
    var back;

    if (fixCell)
    {
        text = '／';
    }
    else
    {
        text = '　';
    }
    color = '#000000';
    back = PrintColor(cell);
    if (fixModeIsOn)
    {
        text = '<button style="color:' + color + ';background-color:' + back + '" onClick="SetFixTile(prdFixTile, ' + x.toString() + ', ' + y.toString() + ')">' + text + '</button>';
    }
    else
    {
        text = '<button style="color:' + color + ';background-color:' + back + '" onClick="OpenTile(prdTile, ' + x.toString() + ', ' + y.toString() + ')">' + text + '</button>';
    }
    return text;
}

function PrintHint(hint)
{
    if (hint == null) return '<button style="color:#e0e0e0;background-color:#e0e0e0">　</button>';

    var text;
    var color;
    var back;

    if (hint.len >= 1)
    {
        text = String.fromCharCode((hint.len).toString().charCodeAt(0) + 0xFEE0);
        //text = ('  ' + hint.len).slice(2);
    }
    else
    {
        text = '  ';
    }
    color = '#e0e0e0';
    back = PrintColor(hint.color);
    text = '<button style="color:' + color + ';background-color:' + back + '">' + text + '</button>';
    return text;
}

function PrintTile(tile)
{
    var text = '';
    var width = tile[0].length;
    var height = tile.length;
    var hintsY = GetHintsY(ansTile);

    for (y = height - 1; y >= 0; y--)
    {
        for (x = 0; x < width; x++)
        {
            text += PrintHint(null);
        }

        for (x = 0; x < width; x++)
        {
            text += PrintHint(hintsY[x][y]);
        }
        text += '<br>';
    }

    for (y = 0; y < height; y++)
    {
        var hintsX = GetHintX(ansTile, y);
        for (x = width - 1; x >= 0; x--)
        {
            text += PrintHint(hintsX[x]);
        }

        for (x = 0; x < width; x++)
        {
            var cell = tile[y][x];
            var fixCell = prdFixTile[y][x];
            text += PrintCell(cell, fixCell, x, y);
        }
        text += '<br>';
    }
    return text;
}
