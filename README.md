# edit-distance

In computational linguistics and computer science, edit distance is a way of quantifying how dissimilar two strings are to one another by counting the minimum number of operations required to transform one string into the other.

This repository aims to not only implement the code but make the user understand the concept of Edit Distance with the help of GUI implementation and a little animation.

### Description of all the files:
* img folder - It consists of all the images(.png) files used in the GUI implementation.

* edit-distance-dynamic-prog.py - This python file contains a simple implementation of Edit Distance using Dynamic Programming without GUI, in case someone wishes to understand the logic of the program while overlooking the GUI aspects of it. This is the fastest way of solving this problem with time complexity of O(mxn), where m and n are the lengths of the two strings.

* edit-distance-gui.py - This python file contains the full code i.e. Edit Distance implementation in Dynamic Programming along with GUI using python tkinter.

* edit-distance-recursion - This python code solves the Edit Distance problem using recursion. This way of solving Edit Distance has a very high time complexity of O(n^3) where n is the length of the longer string. Hence, dynamic programming approach is preferred over this.
