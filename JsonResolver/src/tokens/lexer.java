package tokens;

import java.io.*;
import java.util.ArrayList;

public class lexer {
    public static boolean fault = false;

    static int line = 1;
    static int pos = 0;

    private ArrayList<token> tokens = new ArrayList<>();
    private Reader reader;
    private int _char;

    private char unread_char;
    private boolean unread = false;

    private String flag = "Symbol";

    public lexer(BufferedReader _reader){
        this.reader = _reader;
    }

    private token new_token() throws IOException {
        do{
            next();
        }while (isSpace(_char));
        if(isNull()){
            return new token(token_type.NULL,null, line, pos);
        } else if (_char == ','){
            return new token(token_type.COMMA, ",", line, pos);
        } else if (_char == ':'){
            return new token(token_type.COLON, ":", line, pos);
        } else if (_char == '{') {
            return new token(token_type.START_OBJ, "{", line, pos);
        } else if (_char == '[') {
            return new token(token_type.START_ARRAY, "[", line, pos);
        } else if (_char == ']') {
            return new token(token_type.END_ARRAY, "]", line, pos);
        } else if (_char == '}') {
            return new token(token_type.END_OBJ, "}", line, pos);
        } else if (isTrue()){
            return new token(token_type.BOOLEAN,"true", line, pos);
        } else if (isFalse()){
            return new token(token_type.BOOLEAN,"false", line, pos);
        } else if(_char == '"'){
            flag = "String";
            return str_get();
        } else if(isNum(_char)){
            flag = "Number";
            return num_get();
        } else if (_char == -1) {
            return new token(token_type.END_DOC, "EOF", line, pos);
        } else {
            return new token(token_type.NULL,null, line, pos);
        }
    }

    private void next(){
        try {
            _char = reader.read();
            if(isEnter(_char)){
                next();
                line ++;
                pos = 0;
            }else{
                pos ++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private boolean isSpace(int _char){
        return _char >= 0 && _char <= ' ';
    }

    private boolean isNull(){
        int line_0 = line;
        int pos_0 = pos;
        if(_char== 'n') {
            next();
            if(_char == 'u') {
                next();
                if (_char == 'l') {
                    next();
                    if (_char == 'l') {
                        return true;
                    }
                    else{
                        System.out.println("Line "+line_0+", position "+pos_0+":Invalid null value");
                        fault = true;
                    }
                } else{
                    System.out.println("Line "+line_0+", position "+pos_0+":Invalid null value");
                    fault = true;
                }
            }else{
                System.out.println("Line "+line_0+", position "+pos_0+":Invalid null value");
                fault = true;
            }
        }
        return false;
    }

    private boolean isTrue(){
        int line_0 = line;
        int pos_0 = pos;
        if(_char== 't') {
            next();
            if(_char== 'r') {
                next();
                if (_char == 'u') {
                    next();
                    if (_char == 'e') {
                        return true;
                    }
                    else{
                        System.out.println("Line "+line_0+", position "+pos_0+":Invalid String \"true\"");
                        fault = true;
                    }
                } else{
                    System.out.println("Line "+line_0+", position "+pos_0+":Invalid String \"true\"");
                    fault = true;
                }
            }else{
                System.out.println("Line "+line_0+", position "+pos_0+":Invalid String \"true\"");
                fault = true;
            }
        }
        return false;
    }

    private boolean isFalse() throws IOException{
        int line_0 = line;
        int pos_0 = pos;
        if(_char== 'f') {
            next();
            if(_char== 'a') {
                next();
                if (_char == 'l') {
                    next();
                    if (_char == 's') {
                        next();
                        if(_char == 'e')
                            return true;
                        else{
                            System.out.println("Line "+line_0+", position "+pos_0+":Invalid String \"false\"");
                            fault = true;
                        }
                    } else{
                        System.out.println("Line "+line_0+", position "+pos_0+":Invalid String \"false\"");
                        fault = true;
                    }
                } else{
                    System.out.println("Line "+line_0+", position "+pos_0+":Invalid String \"false\"");
                    fault = true;
                }
            }else{
                System.out.println("Line "+line_0+", position "+pos_0+":Invalid String \"false\"");
                fault = true;
            }
        }
        return false;
    }

    private boolean isNum(int _char){
        return _char >= '0' && _char <= '9' || _char == '-';
    }

    private boolean isExp(int _char){
        return _char == 'e' || _char == 'E';
    }

    private boolean isChar(int _char){
        return  (_char >= 'a' && _char <= 'z') ||
                (_char >= 'A' && _char <= 'Z') || _char == '_'|| _char == '.' ||
                _char == '(' || _char == ')' || _char == '{' || _char == '}' ||
                _char == ',' || _char == '\'' || _char == '/' ||isSpace(_char);
    }

    private boolean isEsc(int _char) {
        if(_char=='\\'){
            next();
            if (_char == '"' || _char == '\\' || _char == '/' || _char == 'b' ||
                    _char == 'f' ||  _char == 't' || _char == 'r' || _char == 'u') {
                return true;
            } else {
                System.out.println("Line "+line+", position "+pos+":Invalid escape value");
                fault = true;
            }
        }
        return false;
    }

    private boolean isEnter(int _char) throws IOException {
        if(_char=='\r'){
            _char = reader.read();
            if ( _char == '\n' ) {
                return true;
            }
        }else if(_char == '\n'){
            return true;
        }
        return false;
    }

    private token num_get() {
        int line_0 = line;
        int pos_0 = pos;
        StringBuilder num = new StringBuilder();
        int dot = 0;
        int exp = 0;
        boolean wrong = false;
        num.append((char) _char);
        while(flag.equals("Number")){
            next();
            char k = (char)_char;
            if(isNum(_char)){
                num.append((char) _char);
            }else if (_char == '.') {
                if(exp!=0){
                    if(!wrong){
                        System.out.println("Line "+line_0+", position "+pos_0+":A number can't contain a \'.\' after \'e\'");
                        fault = true;
                        wrong = true;
                    }
                }
                if(dot == 0){
                    num.append((char)_char);
                    dot = 1;
                }else{
                    if(!wrong){
                        System.out.println("Line "+line_0+", position "+pos_0+":A number can't contain two \'.\'");
                        fault = true;
                        wrong = true;
                    }
                }
            }else if(isExp(_char)) {
                if(exp == 0) {
                    num.append((char) _char);
                    exp = 1;
                }else {
                    if(!wrong){
                        System.out.println("Line "+line_0+", position "+pos_0+":A number can't contain two \'e\'");
                        fault = true;
                        wrong = true;
                    }
                }
            }else if(_char == ','|| _char=='}' ||_char == ']'){
                unread_char = (char)_char;
                unread = true;
                flag = "Symbol";
                return new token(token_type.NUMBER, num.toString(), line, pos_0);
            }else if(_char == '\r'|| _char=='\n' ||_char == '\t'||_char == ' '){
                continue;
            }else{
                if(!wrong){
                    System.out.println("Line "+line+", position "+pos+":This number contains invalid chars");
                    fault = true;
                    wrong = true;
                }
            }
        }
        return new token(token_type.NUMBER, num.toString(), line, pos_0);
    }

    private token str_get() {
        int line_0 = line;
        int pos_0 = pos;
        StringBuilder str = new StringBuilder();
        while (flag.equals("String")) {
            next();
            if (isEsc(_char)) {
                if (_char == 'u') {
                    str.append('\\' + (char)_char);
                    for (int i = 0; i < 4; i++) {
                        next();
                        if (isChar(_char)||isNum(_char)) {
                            str.append((char) _char);
                        } else {
                            System.out.println("Line "+line_0+", position "+pos_0+":Invalid char in string");
                            fault = true;
                        }
                    }
                } else str.append("\\").append((char) _char);
            } else if(isChar(_char)||isNum(_char)){
                str.append((char) _char);
            } else if (_char == '"') {
                flag = "Symbol";
                return new token(token_type.STRING, str.toString(), line_0, pos_0);
            } else if (_char == '\r' || _char == '\n') {
                System.out.println("Line "+line_0+", position "+pos_0+":Invalid escape in string");
                fault = true;
                break;
            } else {
                System.out.println("Line "+line_0+", position "+pos_0+":Invalid char in string or the string isn't end with a \'\"\'");
                fault = true;
                break;
            }
        }
        flag = "Symbol";
        return new token(token_type.STRING, str.toString(), line, pos_0);
    }

    public void create_tokens(){
        try {
            token token;
            do{
                token = new_token();
                tokens.add(token);
                if(unread) {
                    switch (unread_char) {
                        case ',':
                            tokens.add(new token(token_type.COMMA, ",", line, pos));
                            break;
                        case ']':
                            tokens.add(new token(token_type.END_ARRAY, "]", line, pos));
                            break;
                        case '}':
                            tokens.add(new token(token_type.END_OBJ, "}", line, pos));
                            break;
                    }
                    unread = false;
                }
            }while (token.getType()!= token_type.END_DOC);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean isEmpty(){
        return tokens.isEmpty();
    }

    public token next_token() {
        return tokens.remove(0);
    }

    public void pretty(String filename){
        StringBuilder result = new StringBuilder();
        token tok_x;
        int indent = 0;

        for(int i = 0;i<tokens.size();i++){
            tok_x = tokens.get(i);
            switch (tok_x.getType()) {
                case START_OBJ:
                case START_ARRAY:
                    result.append(tok_x.getValue());
                    result.append('\n');
                    indent++;
                    addIndentBlank(result, indent);
                    break;
                case END_OBJ:
                case END_ARRAY:
                    result.append('\n');
                    indent--;
                    addIndentBlank(result, indent);
                    result.append(tok_x.getValue());
                    break;
                case STRING:
                    result.append("\""+tok_x.getValue()+"\"");
                    break;
                case COMMA:
                    result.append(tok_x.getValue());
                    result.append('\n');
                    addIndentBlank(result, indent);
                    break;
                case END_DOC:
                    break;
                default:
                    result.append(tok_x.getValue());
            }
        }
        String path = filename.substring(0,filename.length() - 4) + "pretty.json";
        output(result.toString(),path);
    }

    private static void addIndentBlank(StringBuilder result, int indent) {
        for (int i = 0; i < indent; i++) {
            result.append('\t');
        }
    }

    private void output(String value, String path) {
        File file = new File(path);

        if (!file.exists()) {
            try {
                file.createNewFile();
                FileWriter fw = new FileWriter(file.getAbsoluteFile());
                BufferedWriter bw = new BufferedWriter(fw);
                bw.write(value);
                bw.close();
                System.out.println("Pretty file successfully written!");
            } catch (IOException e1) {
                e1.printStackTrace();
            }
        }
    }
}
