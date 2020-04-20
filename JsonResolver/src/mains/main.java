package mains;

import parse.json_object;
import java.io.FileNotFoundException;

public class main {
    public static void main(String args[]) throws FileNotFoundException {
        operation op = new operation();

        switch (args.length){
            case 1:
                op.resolve(args[0]);
                break;
            case 2:
                if(args[0].equals("-pretty")){
                    op.pretty(args[1]);
                }
                break;
            case 3:
                json_object j_obj = op.resolve(args[0]);
                String path = args[2];
                System.out.println(op.search(path,j_obj));
                break;
            default:
                System.out.println("Usage: java -jar json_resolver.jar [-pretty] fname [-path path]");
        }
    }
}
