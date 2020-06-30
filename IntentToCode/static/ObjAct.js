class Obj {
    constructor(name, isItem, context, x, y, color) {
        this._isItem = isItem;
        this._context = context;
        this._name = name;
        this._startx = x;
        this._starty = y;
        this._x = x;
        this._y = y;
        this._color = color;
        this._disabled = false;
        if (!isItem) {
            grid[x][y] = 0;
        }

    }

    kill() {
        this._disabled = true;
        grid[this._x][this._y] = 1;
    }
    reset() {
        this._disabled = false;
        this._x = this._startx;
        this._y = this._starty;
        grid[this._x][this._y] = 0;
    }

    targetInRange(target) {
        if (Math.abs(this._x - target._x) <= 1 && Math.abs(this._x - target._x) <= 1) {
            return true;
        } else {
            return false;
        }
    }

    drawObj() {
        if (this._isItem) {
            showGameInfo(this._name, "I'm sorry, I'm an item, I can't let you do that.");
            return;
        }
        if (this._disabled) {
            return;
        }
        drawCircle(this._context, this._x * 64, this._y * 64, 32, this._color);
        context.fillStyle = "white";
        this._context.fillText(this._name, this._x * 64 + 5, this._y * 64 + 32);
    }

    cut(target, cutWith) {
        if (this._disabled) {
            showGameInfo(this._name, "I'm dead, cut the reset button to start over");
            return;
        }
        if (this._isItem) {
            showGameInfo(this._name, "I'm sorry, I'm an item, I can't let you do that.");
            return;
        }
        console.log("Cut " + target._name + " with " + cutWith._name);
        if (!cutWith._isItem) {
            showGameInfo(this._name, "I can't cut " + target._name + " with the " + cutWith._name + ". That's just crazy!");
            return;
        } 
        if (this.targetInRange(target)) {
            target.kill();
            showGameInfo(this._name, "I cut the " + target._name + " and destroyed it!");
        } else{
            showGameInfo(this._name, "I can't cut the " + target._name + ". It's to far away.");
        }

    }
    walk(param) {
        if (this._disabled) {
            showGameInfo(this._name, "I'm dead, hit the reset button to start over");
            return;
        }
        if (this._isItem) {
            showGameInfo(this._name, "I'm sorry, I'm an item, I can't let you do that.");
            return;
        }
        grid[this._x][this._y] = 1;
        if(typeof param === "object"){

            this.walkToTarget(param);
            return;
        }
        
        switch (param) {
            case "right":
                if (this._x <= 6 && grid[this._x + 1][this._y] == 1) {
                    this._x += 1;
                } else {
                    showGameInfo(this._name, "I can't walk here!");
                }
                break;
            case "left":
                if (this._x > 0 && grid[this._x - 1][this._y] == 1) {
                    this._x -= 1;
                } else {
                    showGameInfo(this._name, "I can't walk here!");
                }
                break;
            case "up":
                if (this._y > 0 && grid[this._x][this._y - 1] == 1) {
                    this._y -= 1;
                } else {
                    showGameInfo(this._name, "I can't walk here!");
                }
                break;
            case "down":
                if (this._y <= 6 && grid[this._x][this._y + 1] == 1) {
                    this._y += 1;
                } else {
                    showGameInfo(this._name, "I can't walk here!");
                }
                break;
            default:
                break;
        }
        grid[this._x][this._y] = 0;
    }
    jump(direction) {
        if (this._disabled) {
            showGameInfo(this._name, "I'm dead, hit the reset button to start over");
            return;
        }
        if (this._isItem) {
            showGameInfo(this._name, "I'm sorry, I'm an item, I can't let you do that.");
            return;
        }
        //console.log("Jumping " + direction);
        grid[this._x][this._y] = 1;
        if(typeof direction === "object"){
            this.walkToTarget(direction);
            if (this.targetInRange(direction)) {
                showGameInfo(this._name, "What a jump!");
                return;
            } else {
                showGameInfo(this._name, "It is on the other side. Tell me a more precise command. Did you really think it was that simple?");
             }
        }
        switch (direction) {
            case "right":
                if (this._x <= 5 && grid[this._x + 2][this._y] == 1) {
                    this._x += 2;
                } else {
                    showGameInfo(this._name, "I can't jump there!");
                }
                break;
            case "left":
                if (this._x > 1 && grid[this._x - 2][this._y] == 1) {
                    this._x -= 2;
                } else {
                    showGameInfo(this._name, "I can't jump there!");
                }
                break;
            case "up":
                if (this._y > 1 && grid[this._x][this._y - 2] == 1) {
                    this._y -= 2;
                } else {
                    showGameInfo(this._name, "I can't jump there!");
                }
                break;
            case "down":
                if (this._y <= 5 && grid[this._x][this._y + 2] == 1) {
                    this._y += 2;
                } else {
                    showGameInfo(this._name, "I can't jump there!");
                }
                break;
            default:
                break;
        }
        grid[this._x][this._y] = 0;
        
    }
    eat(target) {
        if (this._disabled) {
            showGameInfo(this._name, "I'm dead, hit the reset button to start over");
            return;
        }
        if (this._isItem) {
            showGameInfo(this._name, "I'm sorry, I'm an item, I can't let you do that.");
            return;
        }
        console.log("Eat");
         if (this.targetInRange(target)) {
            target.kill();
            showGameInfo(this._name, "I ate the " + target._name + " and destroyed it!");
        } else{
            showGameInfo(this._name, "I can't eat the " + target._name + ". It's to far away.");
        }
    }
    turn(direction) {
        if (this._disabled) {
            showGameInfo(this._name, "I'm dead, hit the reset button to start over");
            return;
        }
        if (this._isItem) {
            showGameInfo(this._name, "I'm sorry, I'm an item, I can't let you do that.");
            return;
        }
        cosole.log("Turn");
    }

    walkToTarget(target){
        var graph = new Graph(grid);
        var start = graph.grid[this._x][this._y];
        var end = graph.grid[target._x][target._y];
        var result = astar.search(graph, start, end, {closest: true});
        
        if (result.length > 0){
            grid[this._x][this._y] = 1;
            this._x = result[result.length - 1].x;
            this._y = result[result.length - 1].y;
            grid[this._x][this._y] = 0;
        } else{
            console.log("Walked to the same position.");
        }
        
    }
    
}