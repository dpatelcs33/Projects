import jsjf.LinearNode;
import jsjf.LinkedList;

public class InsertionSortLinkedList {

    public static LinkedList insertionSort(LinkedList list) {

        if (list.size() <= 1) {
            return list;
        }

        LinkedList newList = new LinkedList();
        LinearNode newListHead = new LinearNode(list.head.getElement());
        LinearNode current = list.head.getNext();

        while (current != null) {

            LinearNode key = newListHead;
            LinearNode next = current.getNext();

            if ((int) current.getElement() <= (int) newListHead.getElement()){
                LinearNode oldHead = newListHead;
                newListHead = current;
                newListHead.setNext(oldHead);
            }
            else {
                while (key.getNext() != null){

                    if ((int) current.getElement() > (int) key.getElement() && (int) current.getElement() <= (int) key.getNext().getElement()){
                        LinearNode oldNext = key.getNext();
                        key.setNext(current);
                        current.setNext(oldNext);
                    }

                    key = key.getNext();
                }

                if (key.getNext() == null && (int)current.getElement() > (int)key.getElement()) {
                    key.setNext(current);
                    current.setNext(null);
                }
            }

            current = next;
        }

        newList.head = newListHead;
        return newList;
    }
}
