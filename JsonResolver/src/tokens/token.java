package tokens;

public class token {

    private String value;

    private token_type type;

    private int line;

    private int pos;

    public token(token_type type, String value, int line, int pos) {
        this.type = type;
        this.value = value;
        this.line = line;
        this.pos = pos;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public token_type getType() {
        return type;
    }

    public void setType(token_type type) {
        this.type = type;
    }

    public int getLine(){
        return line;
    }

    public void setLine(int _line){
        this.line = _line;
    }

    public int getPos(){
        return pos;
    }

    public void setPos(int _pos){
        this.pos = _pos;
    }
}
