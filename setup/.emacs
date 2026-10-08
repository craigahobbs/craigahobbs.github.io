;;; -*- lexical-binding: t; -*-

;; MacOS?
(when (eq system-type 'darwin)
  ;; set the path - https://www.emacswiki.org/emacs/ExecPath
  (let ((path-from-shell (replace-regexp-in-string
                          "[ \t\n]*$" ""
                          (shell-command-to-string "$SHELL --login -i -c 'echo $PATH'"))))
    (setenv "PATH" path-from-shell)
    (setq exec-path (split-string path-from-shell path-separator)))

  ;; set focus
  (when (display-graphic-p)
    (do-applescript "tell application \"emacs\" to activate"))

  ;; Override Emacs 31.1's -mmacosx-version-min=18.0, which clang rejects during native compilation
  (when (and (fboundp 'native-comp-available-p) (native-comp-available-p))
    (require 'comp)
    (add-to-list 'native-comp-driver-options "-mmacosx-version-min=11")))

;; Package install helpers - errors (e.g. no network) are reported but don't abort init
(require 'package)
(defun my-package-install (package)
  "Install PACKAGE from the package archives, if not already installed."
  (unless (package-installed-p package)
    (condition-case err
        (progn
          (unless (assq package package-archive-contents)
            (package-refresh-contents))
          (package-install package))
      (error (message "Failed to install %s: %s" package (error-message-string err))))))

(defun my-package-install-url (package url)
  "Install PACKAGE from the single-file package at URL, if not already installed."
  (unless (package-installed-p package)
    (condition-case err
        (let ((mode-file (make-temp-file (symbol-name package) nil ".el")))
          (unwind-protect
              (progn
                (url-copy-file url mode-file t)
                (package-install-file mode-file))
            (delete-file mode-file)))
      (error (message "Failed to install %s: %s" package (error-message-string err))))))

;; js2-mode
(my-package-install 'js2-mode)
(add-to-list 'auto-mode-alist '("\\.js\\'" . js2-mode))

;; barescript-mode
(my-package-install-url 'barescript-mode "https://craigahobbs.github.io/bare-script/language/barescript-mode.el")
(add-to-list 'auto-mode-alist '("\\.bare\\'" . barescript-mode))

;; schema-markdown-mode
(my-package-install-url 'schema-markdown-mode "https://craigahobbs.github.io/schema-markdown-js/language/schema-markdown-mode.el")
(add-to-list 'auto-mode-alist '("\\.smd\\'" . schema-markdown-mode))

;; Markdown
(add-to-list 'auto-mode-alist '("\\.md\\'" . text-mode))

;; Activate Savehist mode
(savehist-mode 1)

;; Global toggle-lines command
(global-set-key (kbd "C-x t") 'toggle-truncate-lines)

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
 '(fill-column 120)
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
