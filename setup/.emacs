;; MacOS?
(if (string= system-type "darwin")
    ;; set the path - https://www.emacswiki.org/emacs/ExecPath
    (let ((path-from-shell (replace-regexp-in-string
                            "[ \t\n]*$" ""
                            (shell-command-to-string "$SHELL --login -i -c 'echo $PATH'"))))
      (setenv "PATH" path-from-shell)
      (setq exec-path (split-string path-from-shell path-separator))

      ;; set focus
      (when (display-graphic-p)
        (do-applescript "tell application \"emacs\" to activate")
        )
      )
  )

;; Activate packages
(package-initialize)

;; js2-mode
(unless (package-installed-p 'js2-mode)
  (package-install `js2-mode))
(add-to-list 'auto-mode-alist '("\\.js\\'" . js2-mode))

;; barescript-mode
(unless (package-installed-p 'barescript-mode)
  (let ((mode-file (make-temp-file "barescript-mode")))
    (url-copy-file "https://craigahobbs.github.io/bare-script/language/barescript-mode.el" mode-file t)
    (package-install-file mode-file)
    (delete-file mode-file)))
(add-to-list 'auto-mode-alist '("\\.bare\\'" . barescript-mode))

;; schema-markdown-mode
(unless (package-installed-p 'schema-markdown-mode)
  (let ((mode-file (make-temp-file "schema-markdown-mode")))
    (url-copy-file "https://craigahobbs.github.io/schema-markdown-js/language/schema-markdown-mode.el" mode-file t)
    (package-install-file mode-file)
    (delete-file mode-file)))
(add-to-list 'auto-mode-alist '("\\.smd\\'" . schema-markdown-mode))

;; Markdown
(add-to-list 'auto-mode-alist '("\\.md\\'" . text-mode))

;; Activate Savehist mode
(savehist-mode 1)

;; Global toggle-lines command
(global-set-key "\C-xt" 'toggle-truncate-lines)

;; Enable global upcase/downcase commands
(put 'downcase-region 'disabled nil)
(put 'upcase-region 'disabled nil)


;;;
;;; Customize
;;;
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(auto-save-default nil)
 '(c-basic-offset 4)
 '(column-number-mode t)
 '(compilation-scroll-output t)
 '(compile-command "make ")
 '(default-frame-alist
   '((top . 0)
     (left . 75)
     (width . 120)
     (height . 55)
     (tool-bar-lines . 0)
     (foreground-color . "white")
     (background-color . "black")))
 '(fill-column 100)
 '(global-auto-revert-mode t nil (autorevert))
 '(global-whitespace-mode t)
 '(indent-tabs-mode nil)
 '(inhibit-startup-screen t)
 '(make-backup-files nil)
 '(scroll-conservatively 10000)
 '(sentence-end-double-space nil)
 '(sgml-basic-offset 4)
 '(show-paren-mode t nil (paren))
 '(split-width-threshold nil)
 '(tab-width 4)
 '(truncate-lines t)
 '(whitespace-style
   '(empty face indentation::space space-after-tab space-before-tab tabs trailing)))
