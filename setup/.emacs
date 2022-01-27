;; MacOS?
(if (string= system-type "darwin")
    ;; set the path - https://www.emacswiki.org/emacs/ExecPath
    (let ((path-from-shell (replace-regexp-in-string
                            "[ \t\n]*$" ""
                            (shell-command-to-string "$SHELL --login -i -c 'echo $PATH'"))))
      (setenv "PATH" path-from-shell)
      (setq exec-path (split-string path-from-shell path-separator)))
  )

;; Activate packages
(package-initialize)

;; js2-mode
(unless (package-installed-p 'js2-mode)
  (package-install `js2-mode))
(add-to-list 'auto-mode-alist '("\\.js\\'" . js2-mode))

;; smd-mode
(unless (package-installed-p 'smd-mode)
  (let ((smd-mode-file (make-temp-file "smd-mode")))
    (url-copy-file "https://raw.githubusercontent.com/craigahobbs/schema-markdown/main/extra/smd-mode.el" smd-mode-file t)
    (package-install-file smd-mode-file)
    (delete-file smd-mode-file)))
(add-to-list 'auto-mode-alist '("\\.smd?\\'" . smd-mode))

;; Activate Savehist mode
(savehist-mode 1)

;; Global toggle-lines command
(global-set-key "\C-xt" 'toggle-truncate-lines)

;; Enable global upcase/downcase commands
(put 'downcase-region 'disabled nil)
(put 'upcase-region 'disabled nil)

;; Use text-mode to edit Markdown files
(add-to-list 'auto-mode-alist '("\\.md\\'" . text-mode))


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
 '(default-frame-alist '((width . 120) (height . 55) (tool-bar-lines . 0)))
 '(fill-column 100)
 '(global-auto-revert-mode t nil (autorevert))
 '(global-whitespace-mode t)
 '(indent-tabs-mode nil)
 '(inhibit-startup-screen t)
 '(make-backup-files nil)
 '(package-selected-packages '(smd-mode js2-mode))
 '(scroll-conservatively 10000)
 '(sentence-end-double-space nil)
 '(sgml-basic-offset 4)
 '(show-paren-mode t nil (paren))
 '(split-width-threshold nil)
 '(tab-width 4)
 '(truncate-lines t)
 '(whitespace-style
   '(empty face indentation::space space-after-tab space-before-tab tabs trailing)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(region ((t (:background "sky blue")))))
