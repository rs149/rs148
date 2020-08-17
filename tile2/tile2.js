window.addEventListener('load', () => {

    var frame = document.getElementById('frame');
    
    var inputer = document.getElementById('inputer');
    inputer.addEventListener('click', () => {
        var x = Number(prompt('x'));
        var y = Number(prompt('y'));
        if (Contains(tile, x, y))
        {
            OpenTile(tile, x, y)
            frame.innerHTML = PrintTile(tile);
        }
        else
        {
            alert('OutOfRange');
        }
    }, false);

    frame.innerHTML = PrintTile(tile);
}, false);



var tile = InitTile(25, 25);

function InitTile(width, height)
{
    var tile = [];
    for (y = 0; y < height; y++)
    {
        var row = [];
        for (x = 0; x < width; x++)
        {
            var value = Math.floor(Math.random() * 6);
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

function IsBomb(cell)
{
    return cell == 0 || cell == -11;
}

function GetMines(tile, x, y)
{
    var bombCount = 0;
    var dx, dy;
    for (dy = -1; dy <= 1; dy++)
    {
        for (dx = -1; dx <= 1; dx++)
        {
            if (Contains(tile, x + dx, y + dy) == false) continue;
            var cell = tile[y + dy][x + dx];
            if (IsBomb(cell)) bombCount++;
        }
    }
    return bombCount;
}

function OpenTile(tile, x, y)
{
    //console.log(JSON.stringify(y));
    var cell = tile[y][x];
    if (cell < 0) return;

    if (IsBomb(cell))
    {
        tile[y][x] = -11;
    }
    else
    {
        var mines = GetMines(tile, x, y);
        tile[y][x] = -mines - 1;
        if (mines == 0)
        {
            var dx, dy;
            for (dy = -1; dy <= 1; dy++)
            {
                for (dx = -1; dx <= 1; dx++)
                {
                    if (Contains(tile, x + dx, y + dy) == false) continue;
                    OpenTile(tile, x + dx, y + dy);
                }
            }
        }
    }
    frame.innerHTML = PrintTile(tile);
}

function PrintCell(cell, x, y)
{
    var text;
    if (cell >= 0)
    {
        text = '．';
    }
    else if (cell == -1)
    {
        text = '，';
    }
    else if (cell == -11)
    {
        text = 'Ｘ';
    }
    else
    {
        text = String.fromCharCode((-cell).toString().charCodeAt(0) + 0xFEE0);
    }

    text = '<button onClick="OpenTile(tile, ' + x.toString() + ', ' + y.toString() + ')">' + text + '</button>';
    return text;
}

function PrintTile(tile)
{
    var text = '';
    var width = tile[0].length;
    var height = tile.length;
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            var cell = tile[y][x];
            text += PrintCell(cell, x, y);
        }
        text += '<br>';
    }
    return text;
}