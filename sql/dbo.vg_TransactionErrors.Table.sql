USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_TransactionErrors]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_TransactionErrors](
	[ErrID] [int] IDENTITY(1,1) NOT NULL,
	[InvoiceKey] [int] NOT NULL,
	[ErrResponse] [varchar](50) NULL,
	[ErrMsg] [varchar](500) NULL,
	[ErrDateTime] [smalldatetime] NOT NULL,
	[ErrTypeID] [int] NOT NULL,
 CONSTRAINT [PK_TransactionError_Tbl] PRIMARY KEY CLUSTERED 
(
	[ErrID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_TransactionErrors] ADD  CONSTRAINT [DF_TransactionError_Tbl_ErrDateType]  DEFAULT (getdate()) FOR [ErrDateTime]
GO
ALTER TABLE [dbo].[vg_TransactionErrors] ADD  CONSTRAINT [DF_TransactionError_Tbl_ErrTypeID]  DEFAULT ((-100)) FOR [ErrTypeID]
GO
