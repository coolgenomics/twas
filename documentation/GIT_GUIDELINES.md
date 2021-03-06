# Git Guidelines/Tutorial

A few quick notes on how to use Git.

## Cloning the repo
You can use one of the following commands (first is https, second is over ssh):  
``git clone https://github.com/coolgenomics/twas.git -b master``  
``git clone git@github.com:coolgenomics/twas.git -b master``  
Note that ``-b master`` simply means "clone the master branch". If you wish to
clone a different branch simply change ``master`` to anything else.

## Adding your code
To avoid code clashes in case multiple people are writing code to this repo
simultaneously, pushing code to master should be avoided (although it is not 
explicitly forbidden). Instead do the following:
1. Clone the master branch as demonstrated above
2. Use the following command in the cloned repo to create a new branch (with the
  same code as master) and to switch to that branch.  
  ``git branch <name of new branch>``  
  ``git checkout <name of new branch>``  
  Note that if you get confused you can use ``git branch`` to see which branches
  exist and which one you are on.
3. Once you write some code use the following commands to save the changes to your
  local machine.  
  ``git add .``  
  ``git commit -m "<your commit message>"``  
  You can also check what your changes are with ``git status`` and ``git diff``.
4. Once you've saved the code on your local machine, you should also push it to github.
  That way if your local machine dies, your code lives on! Use:  
  ``git push origin <name of your branch>``  
5. Assuming no one else is writing code to your branch for some weird reason, 
  there shouldn't be any code clashes. However, you will eventually want to put your
  code where other people can use it. First run the following command (while in your
  local repo, on your own branch):
  ``git pull origin master``
  This will try to merge your branch and the master branch and will save the result to
  your branch (you will probably need to use ``git add``, ``git commit``, and ``git
  push``). If there are merge conflicts, you will have to manually resolve them.
  If you are not sure how to do this feel free to ask me!
6. Finally, just go to https://github.com/coolgenomics/twas, click "pull request", "create
  a pull request" and choose "master" as the "base" and your branch as the "compare".
  You can write a little note on the pull request if you want and you can scroll to
  the bottom to see all the changes you are making. Once ready click "create a pull request".
  Then you should be able to approve your own pull request and merge (although it is note
  a bad idea to have someone look at your pull request just in case, especially if you
  are making lots of changes). (Note that if this annoys you you can also just push to
  master, but its nice to do this).
