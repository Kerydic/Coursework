package parse;

import tokens.*;

public class parser {
    public static boolean fault = false;
    private lexer lex;

    public parser(lexer _lex){
        this.lex = _lex;
    }

    public json_object start() {
        if(lex.fault == false){
            if(lex.next_token().getType() == token_type.START_OBJ){
                return (json_object) parse_object(null);
            }else{
                System.out.println("Line 1, position 0:A valid json should begin with a \'{\'!");
                fault = true;
            }
        }else{
           fault = true;
        }
        return null;
    }

    private value parse_object(String obj_name) {
        json_object obj = new json_object(obj_name);
        token tok_x = lex.next_token();
        while(!lex.isEmpty()){
            if(tok_x.getType() == token_type.STRING) {
                String name = tok_x.getValue();
                if (lex.next_token().getType() == token_type.COLON) {
                    tok_x = lex.next_token();
                    switch (tok_x.getType()){
                        case START_OBJ:
                            value val_0 = parse_object(name);
                            obj.add(name, val_0);
                            break;
                        case START_ARRAY:
                            value val_1 = parse_array(name);
                            obj.add(name, val_1);
                            break;
                        case STRING:
                            value val_2 = new json_values(tok_x.getValue(),token_type.STRING);
                            obj.add(name, val_2);
                            break;
                        case NUMBER:
                            value val_3 = new json_values(tok_x.getValue(),token_type.NUMBER);
                            obj.add(name, val_3);
                            break;
                        case BOOLEAN:
                            value val_4 = new json_values(tok_x.getValue(),token_type.BOOLEAN);
                            obj.add(name, val_4);
                            break;
                        case NULL:
                            value val_5 = new json_values(tok_x.getValue(),token_type.NULL);
                            obj.add(name, val_5);
                            break;
                        default:
                            System.out.println("Line "+tok_x.getLine()+", position "+tok_x.getPos()+":The value of object key must be object/array/string/number/boolean/null!");
                            fault = true;
                    }
                    tok_x = lex.next_token();
                    if(tok_x.getType() == token_type.COMMA){
                        tok_x = lex.next_token();
                        continue;
                    }else if(tok_x.getType() == token_type.END_OBJ){
                        break;
                    }else{
                        System.out.println("Line "+tok_x.getLine()+", position "+tok_x.getPos()+":This json object dosen't end with a regular symbol!");
                        fault = true;
                    }
                }else{
                    System.out.println("Line "+tok_x.getLine()+", position "+tok_x.getPos()+":A json object key should have a colon!");
                    fault = true;
                }
            }else{
                System.out.println("Line "+tok_x.getLine()+", position "+tok_x.getPos()+":A json object should have at least one key!");
                fault = true;
            }
        }
        return obj;
    }

    private value parse_array(String name) {
        json_array array = new json_array(name);
        token tok_x = lex.next_token();
        while(!lex.isEmpty()){
            switch (tok_x.getType()){
                case START_OBJ:
                    value val_0 = parse_object(name);
                    array.add(val_0);
                    break;
                case START_ARRAY:
                    value val_1 = parse_array(name);
                    array.add(val_1);
                    break;
                case STRING:
                    value val_2 = new json_values(tok_x.getValue(),token_type.STRING);
                    array.add(val_2);
                    break;
                case NUMBER:
                    value val_3 = new json_values(tok_x.getValue(),token_type.NUMBER);
                    array.add(val_3);
                    break;
                case BOOLEAN:
                    value val_4 = new json_values(tok_x.getValue(),token_type.BOOLEAN);
                    array.add(val_4);
                    break;
                case NULL:
                    value val_5 = new json_values(tok_x.getValue(),token_type.NULL);
                    array.add(val_5);
                    break;
                default:
                    System.out.println("Line "+tok_x.getLine()+", position "+tok_x.getPos()+":The array value must be object/array/string/number/boolean/null!");
                    fault = true;
                    break;
            }
            tok_x = lex.next_token();
            if(tok_x.getType() == token_type.COMMA){
                tok_x = lex.next_token();
                continue;
            }else if(tok_x.getType() == token_type.END_ARRAY){
                break;
            }else{
                System.out.println("Line "+tok_x.getLine()+", position "+tok_x.getPos()+":This json array dosen't end with a regular symbol!");
                fault = true;
            }
        }
        return array;
    }
}
