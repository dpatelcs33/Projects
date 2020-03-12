package jsjf;

import jsjf.exceptions.*;
import java.util.*;

/**
 * LinkedList represents a linked implementation of a list.
 * 
 * @author Java Foundations
 * @version 4.0
 */
public class LinkedList<T> implements ListADT<T>, Iterable<T>
{
    protected int count;
    public LinearNode<T> head, tail;
    protected int modCount;

    /**
     * Creates an empty list.
     */
    public LinkedList()
    {
        count = 0;
        head = tail = null;
        modCount = 0;
    }

    /**
     * Adds a new element to the end of the list.
     * 
     * @param element the element to add.
     */
    public void add(T element) {
        // If the list is empty...
        if(this.tail == null){
            // Creates a new node for the new element.
            LinearNode<T> newElement = new LinearNode(element);
            // Assigns the new node to be the head and the tail.
            this.tail = this.head = newElement;
        } 
        // Otherwise...
        else {
            // Temporary caches the old tail.
            LinearNode<T> temp = this.tail;
            // Creates a new node for the new element.
            LinearNode<T> newElement = new LinearNode(element);
            // Assigns the new node to follow the old tail.
            temp.setNext(newElement);
            // Assigns the old tail to precede the new node.
            newElement.setPrevious(temp);
            // Assigns the new node to be the tail.
            this.tail = newElement;
        }
    }


    /**
     * Adds a new element at a specific index, bumping the current element at 
     * that index to the next index.
     * 
     * @param index the index to add to.
     * @param element the element to add.
     */
    public void add(int index, T element) {
        // Find the node at the index requested.
        LinearNode<T> desiredIndex = this.head;
        for(int i = 1; i <= index; i++){
            desiredIndex = desiredIndex.getNext();
        }
        // Hold the previous element of the old element.
        LinearNode<T> prev = desiredIndex.getPrevious();
        // Create a new node for the new element.
        LinearNode<T> newElement = new LinearNode(element);
        // Assign prev to precede the new element.
        newElement.setPrevious(prev);
        // Assign the old element to follow the new element.
        newElement.setNext(desiredIndex);
        // Assign the new element to precede the old element.
        desiredIndex.setPrevious(newElement);
   }


    /**
     * Returns an element from a specific index, without removing it.
     * 
     * @param index the index to check.
     * @return the element at that index.
     */
    public T get(int index) {
        // Find the node at the index requested.
        LinearNode<T> desiredIndex = this.head;
        for(int i = 1; i <= index; i++){
            desiredIndex = desiredIndex.getNext();
        }
        // Return that element.
        return desiredIndex.getElement();
    }


    /** Removes the first element in this list and returns a reference
     * to it. Throws an EmptyCollectionException if the list is empty.
     *
     * @return a reference to the first element of this list
     * @throws EmptyCollectionException if the list is empty
     */
    public T removeFirst() throws EmptyCollectionException
    {
        if (isEmpty())
            throw new EmptyCollectionException("list");

        T result = head.getElement();
        head = head.getNext();
        count--;

        if(isEmpty())
            tail = null;

        modCount++;

        return result;
    }


    /**
     * Removes the last element in this list and returns a reference
     * to it. Throws an EmptyCollectionException if the list is empty.
     *
     * @return the last element in this list
     * @throws EmptyCollectionException if the list is empty    
     */
    public T removeLast() throws EmptyCollectionException
    {
        if (isEmpty())
            throw new EmptyCollectionException("list");

        T result = tail.getElement();
        tail = tail.getPrevious();
        count--;

        if(isEmpty())
            tail = null;

        modCount++;

        return result;
     }


    /**
     * Removes the first instance of the specified element from this
     * list and returns a reference to it. Throws an EmptyCollectionException 
     * if the list is empty. Throws a ElementNotFoundException if the 
     * specified element is not found in the list.
     *
     * @param  targetElement the element to be removed from the list
     * @return a reference to the removed element
     * @throws EmptyCollectionException if the list is empty
     * @throws ElementNotFoundException if the target element is not found
     */
    public T remove(T targetElement) throws EmptyCollectionException, 
     ElementNotFoundException 
    {
        if (isEmpty())
            throw new EmptyCollectionException("LinkedList");

        boolean found = false;
        LinearNode<T> previous = null;
        LinearNode<T> current = head;

        while (current != null && !found)
            if (targetElement.equals(current.getElement()))
                found = true;
            else
            {
                previous = current;
                current = current.getNext();
            }

        if (!found)
            throw new ElementNotFoundException("LinkedList");

        if (size() == 1)  // only one element in the list
            head = tail = null;
        else if (current.equals(head))  // target is at the head 
            head = current.getNext();
        else if (current.equals(tail))  // target is at the tail
        {
            tail = previous;
            tail.setNext(null);
        }
        else  // target is in the middle
            previous.setNext(current.getNext());

        count--;
        modCount++;

        return current.getElement();
    }


    /**
     * Changes the element at a specific index.
     * 
     * @param index the index to change.
     * @param element the element to change to.
     */
    public void set(int index, T element) {
        // Find the node at the index requested.
        LinearNode<T> desiredIndex = this.head;
        for(int i = 1; i <= index; i++){
            desiredIndex = desiredIndex.getNext();
        }
        // Change the element at that index.
        desiredIndex.setElement(element);
    }


    /**
     * Returns the first element in this list without removing it. 
     *
     * @return the first element in this list
     * @throws EmptyCollectionException if the list is empty
     */
    public T first() throws EmptyCollectionException
    {
        if (isEmpty())
            throw new EmptyCollectionException("list");

        T result = head.getElement();
        return result;
    }


    /**
     * Returns the last element in this list without removing it. 
     *
     * @return the last element in this list  
     * @throws EmptyCollectionException if the list is empty
     */
    public T last() throws EmptyCollectionException
    {
        if (isEmpty())
            throw new EmptyCollectionException("list");

        T result = tail.getElement();
        return result;
    }


    /**
     * Returns true if the specified element is found in this list and 
     * false otherwise. Throws an EmptyCollectionException if the list 
     * is empty.
     *
     * @param  targetElement the element that is sought in the list
     * @return true if the element is found in this list
     * @throws EmptyCollectionException if the list is empty
     */
    public boolean contains(T targetElement) throws 
         EmptyCollectionException 
    {
        if(isEmpty())
            throw new EmptyCollectionException("list");

        boolean found = false;
        LinearNode<T> previous = null;
        LinearNode<T> current = head;

        while (current != null && !found)
            if (targetElement.equals(current.getElement()))
                found = true;
            else
            {
                previous = current;
                current = current.getNext();
            }

        if (!found)
            throw new ElementNotFoundException("LinkedList");

        return found;
    }


    /**
     * Returns true if this list is empty and false otherwise.
     *
     * @return true if the list is empty, false otherwise
     */
    public boolean isEmpty()
    {
        return (count == 0);
    }


    /**
     * Returns the number of elements in this list.
     *
     * @return the number of elements in the list
     */
    public int size()
    {
        return count;
    }


    /**
     * Returns a string representation of this list.
     *
     * @return a string representation of the list    
     */
    public String toString()
    {
        String result = "";
        LinearNode current = head;

        while (current != null)
        {
            result = result + current.getElement() + "\n";
            current = current.getNext();
        }

        return result;
    }


    /**
     * Returns an iterator for the elements in this list. 
     *
     * @return an iterator over the elements of the list
     */
    public Iterator<T> iterator()
    {
        return new LinkedListIterator();
    }


    /**
     * LinkedIterator represents an iterator for a linked list of linear nodes.
     */
    private class LinkedListIterator implements Iterator<T>
    {
        private int iteratorModCount;  // the number of elements in the collection
        private LinearNode<T> current;  // the current position

        /**
         * Sets up this iterator using the specified items.
         *
         * @param collection  the collection the iterator will move over
         * @param size        the integer size of the collection
         */
        public LinkedListIterator()
        {
            current = head;
            iteratorModCount = modCount;
        }

        /**
         * Returns true if this iterator has at least one more element
         * to deliver in the iteration.
         *
         * @return  true if this iterator has at least one more element to deliver
         *          in the iteration
         * @throws  ConcurrentModificationException if the collection has changed
         *          while the iterator is in use
         */
        public boolean hasNext() throws ConcurrentModificationException
        {
            if (iteratorModCount != modCount) 
                throw new ConcurrentModificationException();

            return (current != null);
        }

        /**
         * Returns the next element in the iteration. If there are no
         * more elements in this iteration, a NoSuchElementException is
         * thrown.
         *
         * @return the next element in the iteration
         * @throws NoSuchElementException if the iterator is empty
         */
        public T next() throws ConcurrentModificationException
        {
            if (!hasNext())
                throw new NoSuchElementException();

            T result = current.getElement();
            current = current.getNext();
            return result;
        }

        /**
         * The remove operation is not supported.
         * 
         * @throws UnsupportedOperationException if the remove operation is called
         */
        public void remove() throws UnsupportedOperationException
        {
            throw new UnsupportedOperationException();
        }
    }

}