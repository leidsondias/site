---
title: "Help him!! Help your code reviewer."
tags: ['Code Review', 'Git']
date: 2020-10-25T22:33:46.318000
---

![Photo by [AltumCode](https://unsplash.com/@altumcode?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/code-reviewer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)](https://cdn-images-1.medium.com/max/2000/1*G7iDYc0kqrfTAbzzaiPiHg.jpeg)*Photo by [AltumCode](https://unsplash.com/@altumcode?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/code-reviewer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)*

Recently, I did a talk about Git to colleagues from my new work. The objective was to pass my learnings about Git to them. I learned a lot of Git in my last company. Not just commands but how to make our life easy when we do code review.

The main goal of this post is what you can do to make easy the life of your code reviewer. What commands you can use, practices, etc.

**PS**: This is my opinion you aren’t obliged to agree. We can always discuss it.

## What is Git?

So, to start, let me give you a little explanation of what Git is. Git is a version control system. It is the most used system for versioning. You can check other version control systems (SVN, CVS, etc).

## What is a Commit? Why is important to have a well commit message?

This command captures a snapshot of the currently staged changes from the project.

Some projects are legacy or have a lot of people contributing it. So, if you are a rookie on the project or you want to know why the changes were made you can read the commits to understand.

Therefore, we should write a good commits message to help other developers and to make it easier to do the code review. So, the **first tip** to help the code reviewer is: **write well commits messages**.

## Commits good practices

A commit should be a wrapper for related changes. For example, creating two different components should produce two separate commits. Produce small commits make it easier for other developers/code reviewers to understand the changes and what context/concern the commit is related to or roll back the changes if something went wrong.

The **second tip** is: create small commits but always being a wrapper for related changes without mixing concerns.

The **third tip** never a commit should be a broken commit. Your commit needs to works lonely if it’s needed. You can have WIP commits, but remember to complete the commits before you when open the PR.

This tip is related by roll back the changes if something went wrong, for you don’t have any risk to go to another commit.

I see a lot of people want to create a new commit just for the tests. Don’t do it. Following the commit pattern about being a wrapper of related things and working itself, if you create a new commit for a test your old commit will contain wrong things and don’t work alone.

The **fourth** tip is to use the **fixup** command during the review process. This is a very interesting command and for me, very powerful to make easier the reviewer’s life.

The **fixup** command creates a new one commit but is a child for another one. If you do the **rebase** with **squash**, you will merge the child commit to the parent commit. For example, the reviewer found a bug and you correct it. The normal is to create a new commit to fix the last commit, but if you do this your last commit will contain a bug and you will have a commit with a problem in your branch. So, we create a fixup commit, and after the reviewer validates the changes you can squash it in the parent commit.

Below you can see some interesting links about how to write good commit messages and patterns.

1. [https://chris.beams.io/posts/git-commit/](https://chris.beams.io/posts/git-commit/)

1. [https://github.com/trein/dev-best-practices/wiki/Git-Commit-Best-Practices](https://github.com/trein/dev-best-practices/wiki/Git-Commit-Best-Practices)

I hope this post helps you to think about your Git process and helps to think more about how to use Git most efficiently.

The original post is https://medium.com/@leidson/help-him-help-your-code-reviewer-5ce1d68289c4
