package mains;

import parse.json_object;
import parse.parser;
import parse.value;
import tokens.lexer;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;

class operation {
    json_object resolve(String path) throws FileNotFoundException {
        BufferedReader in = new BufferedReader(new FileReader(path));
        lexer le = new lexer(in);
        le.create_tokens();
        parser p = new parser(le);
        json_object obj = p.start();
        if(p.fault == false){
            System.out.println("Valid");
        }
        return obj;
    }

    void pretty(String path) throws FileNotFoundException {
        lexer le_for_parse = new lexer(new BufferedReader(new FileReader(path)));
        le_for_parse.create_tokens();
        lexer le_for_pretty = new lexer(new BufferedReader(new FileReader(path)));
        le_for_pretty.create_tokens();
        parser p = new parser(le_for_parse);
        json_object obj = p.start();
        if(p.fault == false){
            System.out.println("Valid");
        }
        le_for_pretty.pretty(path);
    }

    String search(String path, json_object obj){
        String[] path_array = path.split("/");
        value val_1 = obj;
        value val_2;
        for(int i = 1;i<path_array.length;i++){
            if(isNull(val_1)){
                return null;
            }
            if(path_array[i].contains("[")) {
                String exp = path_array[i];
                String array_name = exp.substring(0,exp.indexOf("["));
                int key = Integer.parseInt(exp.substring(exp.indexOf("[")+1,exp.indexOf("]"))) - 1;
                val_2 = val_1.get_value(array_name).get_value(Integer.toString(key));
                val_1 = val_2;
            }else{
                String val_name = path_array[i];
                val_2 = val_1.get_value(val_name);
                val_1 = val_2;
            }
        }
        return val_1.toString();
    }

    private boolean isNull(value val){
        return val == null;
    }
}
