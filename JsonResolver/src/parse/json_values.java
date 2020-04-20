package parse;

import tokens.token_type;

public class json_values implements value{
    String value;
    token_type type;

    public json_values(String _value, token_type _type){
        this.value = _value;
        this.type = _type;
    }

    public String toString(){
        return value;
    }

    public token_type getJSONType(){
        return type;
    }

    public value get_value(String _key){
        return this;
    }
}
